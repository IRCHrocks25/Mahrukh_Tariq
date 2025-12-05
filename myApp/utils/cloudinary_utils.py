import cloudinary
import cloudinary.uploader
from io import BytesIO
from PIL import Image
import os

# Smart compression function - converts to WebP
def smart_compress_to_bytes(image_file, max_bytes=10 * 1024 * 1024, target_bytes=None):
    """
    Compress image to target size while maintaining quality.
    Converts image to WebP format before upload.
    Returns BytesIO object with compressed WebP image.
    """
    if target_bytes is None:
        target_bytes = int(max_bytes * 0.93)  # 93% of max
    
    # Open image
    img = Image.open(image_file)
    
    # Convert RGBA to RGB if necessary (WebP supports transparency, but we'll handle it)
    # For WebP, we can keep RGBA mode as it supports transparency
    if img.mode == 'P':
        img = img.convert('RGBA')
    elif img.mode not in ('RGB', 'RGBA'):
        # Convert other modes to RGB
        if img.mode in ('LA',):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'LA':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        else:
            img = img.convert('RGB')
    
    # Get current size with WebP
    output = BytesIO()
    # Save as WebP with high quality first
    img.save(output, format='WEBP', quality=95, method=6)
    current_size = output.tell()
    
    # If already under target, return
    if current_size <= target_bytes:
        output.seek(0)
        return output
    
    # Binary search for quality
    min_quality = 10
    max_quality = 95
    best_output = None
    
    while min_quality <= max_quality:
        quality = (min_quality + max_quality) // 2
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, method=6)
        size = output.tell()
        
        if size <= target_bytes:
            best_output = output
            min_quality = quality + 1
        else:
            max_quality = quality - 1
    
    if best_output:
        best_output.seek(0)
        return best_output
    
    # If still too large, resize
    output = BytesIO()
    scale = (target_bytes / current_size) ** 0.5
    new_size = (int(img.width * scale), int(img.height * scale))
    img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
    img_resized.save(output, format='WEBP', quality=85, method=6)
    output.seek(0)
    return output

def upload_to_cloudinary(image_file, folder='garden_gate', public_id=None):
    """
    Process: Image → Convert to WebP → Upload to Cloudinary → Return URL
    
    Steps:
    1. Image is opened and processed
    2. Converted to WebP format with compression
    3. Uploaded to Cloudinary (already in WebP format)
    4. Returns secure URL and variants
    
    Returns dict with URLs and metadata.
    """
    # Step 1 & 2: Compress and convert image to WebP
    compressed_webp = smart_compress_to_bytes(image_file)
    
    # Get filename
    filename = image_file.name if hasattr(image_file, 'name') else 'image.jpg'
    name_without_ext = os.path.splitext(filename)[0]
    
    # Step 3: Upload WebP to Cloudinary (already in WebP format)
    upload_result = cloudinary.uploader.upload(
        compressed_webp,
        folder=folder,
        public_id=public_id or name_without_ext,
        resource_type='image',
        format='webp',  # Already WebP, but specify for clarity
        transformation=[
            {'quality': 'auto'},
            {'fetch_format': 'auto'}
        ],
        access_mode='public'
    )
    
    # Generate URLs
    secure_url = upload_result['secure_url']
    public_id = upload_result['public_id']
    
    # Web-optimized URL
    web_url = secure_url.replace('/upload/', '/upload/f_webp,q_80,w_1920/')
    
    # Thumbnail URL
    thumb_url = secure_url.replace('/upload/', '/upload/f_webp,q_80,w_400/')
    
    return {
        'url': upload_result['url'],
        'secure_url': secure_url,
        'public_id': public_id,
        'web_url': web_url,
        'thumb_url': thumb_url,
        'width': upload_result.get('width'),
        'height': upload_result.get('height'),
        'format': upload_result.get('format'),
        'bytes': upload_result.get('bytes'),
    }

