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
    
    # Preserve transparency - convert to RGBA if image has transparency
    # WebP supports transparency, so we keep RGBA mode
    if img.mode == 'P':
        # Palette mode - check if it has transparency
        if 'transparency' in img.info:
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    elif img.mode == 'LA':
        # Grayscale with alpha
        img = img.convert('RGBA')
    elif img.mode not in ('RGB', 'RGBA'):
        # For other modes, try to preserve transparency if possible
        if hasattr(img, 'mode') and 'A' in img.mode or img.mode in ('RGBA', 'LA'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    
    # Get current size with WebP
    output = BytesIO()
    # Save as WebP with high quality first, preserving transparency
    save_kwargs = {'format': 'WEBP', 'quality': 95, 'method': 6}
    if img.mode == 'RGBA':
        # Ensure lossless transparency is preserved
        save_kwargs['lossless'] = False  # Use lossy but preserve alpha
    img.save(output, **save_kwargs)
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
        save_kwargs = {'format': 'WEBP', 'quality': quality, 'method': 6}
        if img.mode == 'RGBA':
            save_kwargs['lossless'] = False  # Preserve alpha channel
        img.save(output, **save_kwargs)
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
    save_kwargs = {'format': 'WEBP', 'quality': 85, 'method': 6}
    if img_resized.mode == 'RGBA':
        save_kwargs['lossless'] = False  # Preserve alpha channel
    img_resized.save(output, **save_kwargs)
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
    # Check if image has transparency by checking mode
    compressed_webp.seek(0)  # Reset to beginning
    img_check = Image.open(compressed_webp)
    has_transparency = img_check.mode == 'RGBA'
    compressed_webp.seek(0)  # Reset to beginning again after reading
    
    # Build transformation list
    transformations = [{'quality': 'auto'}]
    if has_transparency:
        transformations.append({'fetch_format': 'webp'})
    else:
        transformations.append({'fetch_format': 'auto'})
    
    # Build upload kwargs
    upload_kwargs = {
        'folder': folder,
        'public_id': public_id or name_without_ext,
        'resource_type': 'image',
        'format': 'webp',
        'transformation': transformations,
        'access_mode': 'public'
    }
    
    upload_result = cloudinary.uploader.upload(
        compressed_webp,
        **upload_kwargs
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

