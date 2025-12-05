from django.db import models

# Model to store image URLs for different sections
class SectionImage(models.Model):
    section_name = models.CharField(max_length=100, unique=True, help_text="Internal name for the section (e.g., 'hero_background', 'about_image')")
    display_name = models.CharField(max_length=200, help_text="Display name shown in dashboard")
    image_url = models.URLField(blank=True, null=True, help_text="Image URL")
    image_alt = models.CharField(max_length=200, blank=True, help_text="Alt text for the image")
    icon_url = models.URLField(blank=True, null=True, help_text="Icon URL (if applicable)")
    background_image_url = models.URLField(blank=True, null=True, help_text="Background image URL (if applicable)")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_name']
        verbose_name = "Section Image"
        verbose_name_plural = "Section Images"
    
    def __str__(self):
        return self.display_name

# Model to store uploaded images in gallery
class MediaAsset(models.Model):
    url = models.URLField(help_text="Cloudinary URL")
    secure_url = models.URLField(help_text="Secure Cloudinary URL")
    public_id = models.CharField(max_length=500, help_text="Cloudinary public ID")
    folder = models.CharField(max_length=200, blank=True, help_text="Cloudinary folder")
    filename = models.CharField(max_length=200, blank=True, help_text="Original filename")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Media Asset"
        verbose_name_plural = "Media Assets"
    
    @property
    def thumb_url(self):
        """Generate thumbnail URL"""
        return self.secure_url.replace('/upload/', '/upload/f_webp,q_80,w_400/')
    
    def __str__(self):
        return self.filename or self.public_id
