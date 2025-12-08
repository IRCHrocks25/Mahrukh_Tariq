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

# Model to store services section content
class ServiceCard(models.Model):
    card_number = models.IntegerField(unique=True, help_text="Card number (1, 2, or 3)")
    title = models.CharField(max_length=200, help_text="Service card title")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Service card subtitle")
    image_url = models.URLField(blank=True, null=True, help_text="Card image URL")
    image_alt = models.CharField(max_length=200, blank=True, help_text="Image alt text")
    features = models.TextField(help_text="Features list (one per line)")
    result_text = models.CharField(max_length=300, help_text="Result text")
    cta_text = models.CharField(max_length=100, default="Learn More", help_text="Call to action text")
    cta_link = models.CharField(max_length=200, default="#consultation", help_text="Call to action link")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['card_number']
        verbose_name = "Service Card"
        verbose_name_plural = "Service Cards"
    
    def __str__(self):
        return f"Service Card {self.card_number}: {self.title}"
    
    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]

# Model to store services section header
class ServicesSection(models.Model):
    title = models.CharField(max_length=200, default="Management That Fits Your Goals.")
    description = models.TextField(default="Every landlord is different. Some want complete freedom. Others prefer involvement. We tailor our service to fit you.")
    cta_text = models.CharField(max_length=100, default="Find Your Fit")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Services Section"
        verbose_name_plural = "Services Section"
    
    def __str__(self):
        return "Services Section"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Get or create the single instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj