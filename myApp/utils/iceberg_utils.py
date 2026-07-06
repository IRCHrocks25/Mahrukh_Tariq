"""
Iceberg CDN (Katalyst) upload utility.

Server-to-server flow (bytes never traverse the API):
  1. POST {API_BASE}/assets/init-upload  -> presigned R2 URL
  2. PUT bytes directly to the presigned URL
  3. POST {API_BASE}/assets/complete     -> Iceberg HEADs R2 + flips the row

Configuration (.env):
  ICEBERG_API_TOKEN  - API token minted in the Katalyst dashboard ("kic_...")
  ICEBERG_API_BASE   - optional, defaults to https://dashboard.katalyst-crm.com
  ICEBERG_CDN_BASE   - optional fallback used to build the public URL when the
                       API response doesn't include one,
                       e.g. https://cdn.katalyst-crm.com/t1
"""
import os
import uuid
from io import BytesIO

import requests
from PIL import Image

DEFAULT_API_BASE = 'https://dashboard.katalyst-crm.com'
DEFAULT_CDN_BASE = 'https://cdn.katalyst-crm.com'


# Smart compression function - converts to WebP
def smart_compress_to_bytes(image_file, max_bytes=10 * 1024 * 1024, target_bytes=None):
    """
    Compress image to target size while maintaining quality.
    Converts image to WebP format before upload.
    Returns BytesIO object with compressed WebP image.
    """
    if target_bytes is None:
        target_bytes = int(max_bytes * 0.93)  # 93% of max

    img = Image.open(image_file)

    # Preserve transparency - WebP supports alpha, so keep RGBA where present
    if img.mode == 'P':
        if 'transparency' in img.info:
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    elif img.mode == 'LA':
        img = img.convert('RGBA')
    elif img.mode not in ('RGB', 'RGBA'):
        if 'A' in img.mode:
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')

    output = BytesIO()
    save_kwargs = {'format': 'WEBP', 'quality': 95, 'method': 6}
    img.save(output, **save_kwargs)
    current_size = output.tell()

    if current_size <= target_bytes:
        output.seek(0)
        return output

    # Binary search for quality
    min_quality, max_quality = 10, 95
    best_output = None
    while min_quality <= max_quality:
        quality = (min_quality + max_quality) // 2
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, method=6)
        if output.tell() <= target_bytes:
            best_output = output
            min_quality = quality + 1
        else:
            max_quality = quality - 1

    if best_output:
        best_output.seek(0)
        return best_output

    # Still too large: resize
    output = BytesIO()
    scale = (target_bytes / current_size) ** 0.5
    new_size = (int(img.width * scale), int(img.height * scale))
    img.resize(new_size, Image.Resampling.LANCZOS).save(output, format='WEBP', quality=85, method=6)
    output.seek(0)
    return output


def _get_token():
    return os.getenv('ICEBERG_API_TOKEN', '').strip()


def is_configured():
    return bool(_get_token())


def _pick(data, *names):
    """Return the first matching key from a (possibly nested) API response."""
    if not isinstance(data, dict):
        return None
    for name in names:
        if data.get(name):
            return data[name]
    # one level of nesting (e.g. {"asset": {...}} or {"data": {...}})
    for value in data.values():
        if isinstance(value, dict):
            found = _pick(value, *names)
            if found:
                return found
    return None


def upload_to_iceberg(image_file, folder='garden_gate'):
    """
    Compress to WebP and upload via the Iceberg presigned three-step flow.
    Returns a dict shaped like the old Cloudinary result:
    url / secure_url / public_id / web_url / thumb_url.
    """
    token = _get_token()
    if not token:
        raise RuntimeError('ICEBERG_API_TOKEN is not set. Mint an API token in the '
                           'Katalyst dashboard and add it to your .env file.')

    api_base = os.getenv('ICEBERG_API_BASE', DEFAULT_API_BASE).rstrip('/')
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # Compress to WebP
    compressed = smart_compress_to_bytes(image_file)
    body = compressed.read()

    # Unique object key so uploads never overwrite each other
    filename = getattr(image_file, 'name', 'image.jpg')
    name = os.path.splitext(os.path.basename(filename))[0]
    safe_name = ''.join(c if c.isalnum() or c in '-_' else '-' for c in name).strip('-') or 'image'
    key = f"{folder.strip('/')}/{safe_name}-{uuid.uuid4().hex[:8]}.webp"
    content_type = 'image/webp'

    # 1. Init upload -> presigned R2 URL
    resp = requests.post(
        f'{api_base}/assets/init-upload',
        headers=headers,
        json={'key': key, 'content_type': content_type},
        timeout=30,
    )
    resp.raise_for_status()
    init_data = resp.json()
    upload_url = _pick(init_data, 'upload_url', 'uploadUrl', 'presigned_url', 'presignedUrl', 'put_url', 'url')
    if not upload_url:
        raise RuntimeError(f'init-upload response did not contain an upload URL: {init_data}')

    # 2. PUT the bytes directly to R2
    put_resp = requests.put(upload_url, data=body, headers={'Content-Type': content_type}, timeout=120)
    put_resp.raise_for_status()

    # 3. Mark ready
    resp = requests.post(f'{api_base}/assets/complete', headers=headers, json={'key': key}, timeout=30)
    resp.raise_for_status()
    complete_data = {}
    try:
        complete_data = resp.json()
    except ValueError:
        pass

    # Public URL: prefer one from the API; otherwise build it as
    # {CDN base}/{tenant id}/{key} — the tenant id comes back from both
    # init-upload (tenant_id) and complete (TenantID).
    public_url = (
        _pick(complete_data, 'public_url', 'publicUrl', 'cdn_url', 'cdnUrl', 'url')
        or _pick(init_data, 'public_url', 'publicUrl', 'cdn_url', 'cdnUrl')
    )
    if not public_url:
        tenant = (
            _pick(complete_data, 'TenantID', 'tenant_id', 'tenantId')
            or _pick(init_data, 'tenant_id', 'TenantID', 'tenantId')
            or os.getenv('ICEBERG_TENANT_SEGMENT', '')
        ).strip('/')
        cdn_base = os.getenv('ICEBERG_CDN_BASE', DEFAULT_CDN_BASE).rstrip('/')
        public_url = '/'.join(p for p in [cdn_base, tenant, key] if p)

    return {
        'url': public_url,
        'secure_url': public_url,
        'public_id': key,
        'web_url': public_url,
        'thumb_url': public_url,
        'bytes': len(body),
    }
