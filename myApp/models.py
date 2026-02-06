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

# Model to store Hero section content
class HeroSection(models.Model):
    title = models.CharField(max_length=300, default="Stop Losing Money to Property Managers Who Don't Care.")
    subtitle = models.CharField(max_length=200, default="Your Investment Deserves an Owner's Standard.")
    description = models.TextField(default="Most property management firms treat you like another number. At Garden Gate, you work directly with me – Mahrukh Tariq. I manage your property with the same standards I apply to my own 90-unit portfolio: honest pricing, rigorous tenant screening, and personal attention that corporations can't replicate.")
    cta_text = models.CharField(max_length=100, default="Show Me How This Actually Works")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"
    
    def __str__(self):
        return "Hero Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Credibility section content
class CredibilitySection(models.Model):
    title = models.CharField(max_length=300, default="Proven Experience. Personal Commitment.<br>Real Results.")
    description = models.TextField(default="Garden Gate is not a franchise or volume-driven agency. It's a boutique property management firm built on 13 years of hands-on real estate experience — backed by a personal portfolio that proves its systems deliver results.")
    subtitle = models.CharField(max_length=200, default="Why Landlords Choose Garden Gate")
    subtitle_description = models.TextField(default="Most property managers have never been landlords. Mahrukh Tariq is both. Here's why that matters to your bottom line:")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Credibility Section"
        verbose_name_plural = "Credibility Section"
    
    def __str__(self):
        return "Credibility Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Credibility cards
class CredibilityCard(models.Model):
    card_number = models.IntegerField(unique=True, help_text="Card number (1, 2, 3, or 4)")
    title = models.CharField(max_length=200, help_text="Card title")
    description = models.TextField(help_text="Card description")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['card_number']
        verbose_name = "Credibility Card"
        verbose_name_plural = "Credibility Cards"
    
    def __str__(self):
        return f"Credibility Card {self.card_number}: {self.title}"

# Model to store Testimonials section header
class TestimonialsSection(models.Model):
    title = models.CharField(max_length=200, default="Why Landlords Stop Looking After Finding Us")
    cta_text = models.CharField(max_length=100, default="Find Out If We're the Right Fit")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Testimonials Section"
        verbose_name_plural = "Testimonials Section"
    
    def __str__(self):
        return "Testimonials Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store individual testimonials
class Testimonial(models.Model):
    testimonial_number = models.IntegerField(unique=True, help_text="Testimonial number (1, 2, or 3)")
    avatar_url = models.URLField(blank=True, null=True, help_text="Avatar image URL")
    avatar_alt = models.CharField(max_length=200, blank=True, help_text="Avatar alt text")
    quote_short = models.CharField(max_length=300, help_text="Short quote (italic)")
    quote_long = models.TextField(help_text="Long quote/description")
    author_name = models.CharField(max_length=100, help_text="Author name")
    author_title = models.CharField(max_length=200, help_text="Author title/location")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['testimonial_number']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"Testimonial {self.testimonial_number}: {self.author_name}"

# Model to store Statistics section content
class StatisticsSection(models.Model):
    title = models.CharField(max_length=200, default="Why Quality Management Matters")
    subtitle = models.CharField(max_length=200, default="The Cost of Poor Management:")
    point_1 = models.CharField(max_length=300, default="Long vacancies that cost thousands in lost rent.")
    point_2 = models.CharField(max_length=300, default="Vendor markups of 10–25% on maintenance invoices.")
    point_3 = models.CharField(max_length=300, default="Unresponsive managers — 29% of tenants report landlords are \"slow to get things done.\"")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Statistics Section"
        verbose_name_plural = "Statistics Section"
    
    def __str__(self):
        return "Statistics Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Pain Points section content
class PainPointsSection(models.Model):
    title = models.CharField(max_length=200, default="Common Problems.<br>Clear Solutions.")
    description = models.TextField(default="Owning rental property shouldn't mean chasing managers or worrying about surprise bills. But too often, landlords deal with:")
    pain_point_1 = models.CharField(max_length=200, default="Managers who disappear when you need answers.")
    pain_point_2 = models.CharField(max_length=200, default="Inflated maintenance costs and hidden markups.")
    pain_point_3 = models.CharField(max_length=200, default="Weak screening that lets in problem tenants.")
    pain_point_4 = models.CharField(max_length=200, default="Generic, one-size-fits-all service.")
    pain_point_5 = models.CharField(max_length=200, default="Unapproved expenses with zero transparency.")
    solution_1 = models.CharField(max_length=300, default="<strong class=\"text-gold italic\">Immediate Access</strong> — You call. I answer. Same day.")
    solution_2 = models.CharField(max_length=300, default="<strong class=\"text-gold italic\">Transparent Pricing</strong> — You review every estimate before work begins.")
    solution_3 = models.CharField(max_length=300, default="<strong class=\"text-gold italic\">Rigorous Screening</strong> — Every tenant meets me personally before approval.")
    solution_4 = models.CharField(max_length=300, default="<strong class=\"text-gold italic\">Customized Management</strong> — Your goals, your preferences, your plan.")
    solution_5 = models.CharField(max_length=300, default="<strong class=\"text-gold italic\">Total Transparency</strong> — You're informed before money moves. Always.")
    cta_text = models.CharField(max_length=100, default="Get a Free Rental Analysis")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pain Points Section"
        verbose_name_plural = "Pain Points Section"
    
    def __str__(self):
        return "Pain Points Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Methodology section content
class MethodologySection(models.Model):
    title = models.CharField(max_length=200, default="The Garden Gate Framework")
    description = models.TextField(default="Most companies chase volume. We build relationships. Every property receives personalized attention, open communication, and proactive care.")
    cta_text = models.CharField(max_length=100, default="See the Framework in Action")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Methodology Section"
        verbose_name_plural = "Methodology Section"
    
    def __str__(self):
        return "Methodology Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Methodology steps
class MethodologyStep(models.Model):
    step_number = models.IntegerField(unique=True, help_text="Step number (1-5)")
    title = models.CharField(max_length=100, help_text="Step title (e.g., 'Assessment')")
    description = models.TextField(help_text="Step description")
    result_text = models.CharField(max_length=200, help_text="Result text")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['step_number']
        verbose_name = "Methodology Step"
        verbose_name_plural = "Methodology Steps"
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"

# Model to store About section content
class AboutSection(models.Model):
    title = models.CharField(max_length=200, default="I Built This Because I Was You")
    content = models.TextField(help_text="Main content paragraphs (one per line)")
    quote_text = models.CharField(max_length=300, default="I don't lock clients in. I earn their trust, one transparent decision at a time.")
    quote_author = models.CharField(max_length=100, default="— Mahrukh Tariq")
    cta_text = models.CharField(max_length=100, default="See If We're a Fit")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"
    
    def __str__(self):
        return "About Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def get_content_paragraphs(self):
        """Return content as a list of paragraphs"""
        return [p.strip() for p in self.content.split('\n') if p.strip()]

# Model to store Mission/Vision section content
class MissionVisionSection(models.Model):
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_subtitle = models.CharField(max_length=200, default="Deliver What Corporate Management Can't.")
    mission_description = models.TextField(default="We exist because landlords deserve better — direct access, transparent pricing, and genuine partnership. Garden Gate gives you clarity, control, and confidence in your investment.")
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_subtitle = models.CharField(max_length=200, default="Boutique Management That Puts Landlords First.")
    vision_description = models.TextField(default="We're building Northern Virginia's most trusted boutique property management firm — where landlords enjoy ownership, not endure it.")
    cta_text = models.CharField(max_length=100, default="Join Us")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mission/Vision Section"
        verbose_name_plural = "Mission/Vision Section"
    
    def __str__(self):
        return "Mission/Vision Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Lead Magnet section content
class LeadMagnetSection(models.Model):
    title = models.CharField(max_length=200, default="Free 15 Minute Property<br>Assessment")
    subtitle = models.CharField(max_length=200, default="No sales pitch. Just straight answers to:")
    bullet_1 = models.CharField(max_length=200, default="What your property should actually rent for")
    bullet_2 = models.CharField(max_length=200, default="Where you're currently losing money")
    bullet_3 = models.CharField(max_length=200, default="Whether we're a good fit (honest answer)")
    description = models.TextField(default="If we're not right for you, I'll tell you. If we are, you'll know exactly what happens next.")
    cta_text = models.CharField(max_length=100, default="Show Me How This Actually Works")
    cta_link = models.CharField(max_length=200, default="#consultation")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Lead Magnet Section"
        verbose_name_plural = "Lead Magnet Section"
    
    def __str__(self):
        return "Lead Magnet Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Final CTA section content
class FinalCTASection(models.Model):
    title = models.CharField(max_length=200, default="Stop Settling. Start Succeeding.")
    description = models.TextField(default="While others chase unresponsive managers and inflated repair bills, you can work with someone who treats your property like her own.")
    cta_text = models.CharField(max_length=100, default="Show Me How This Actually Works")
    cta_link = models.CharField(max_length=200, default="#contact")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Final CTA Section"
        verbose_name_plural = "Final CTA Section"
    
    def __str__(self):
        return "Final CTA Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Blog section header
class BlogSection(models.Model):
    title = models.CharField(max_length=200, default="Insights & Expertise")
    subtitle = models.CharField(max_length=300, default="Learn from our experience managing properties and building successful landlord relationships.")
    cta_text = models.CharField(max_length=100, default="View All Posts")
    cta_link = models.CharField(max_length=200, default="#blog")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Blog Section"
        verbose_name_plural = "Blog Section"
    
    def __str__(self):
        return "Blog Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Blog Posts
class BlogPost(models.Model):
    title = models.CharField(max_length=300, help_text="Blog post title")
    slug = models.SlugField(max_length=300, unique=True, help_text="URL-friendly version of title")
    excerpt = models.TextField(max_length=500, help_text="Short excerpt/preview text")
    content = models.TextField(help_text="Full blog post content")
    featured_image_url = models.URLField(blank=True, null=True, help_text="Featured image URL")
    featured_image_alt = models.CharField(max_length=200, blank=True, help_text="Featured image alt text")
    author_name = models.CharField(max_length=100, default="Mahrukh Tariq", help_text="Author name")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Publication date")
    updated_date = models.DateTimeField(auto_now=True, help_text="Last update date")
    is_featured = models.BooleanField(default=False, help_text="Show in featured section")
    is_published = models.BooleanField(default=True, help_text="Published status")
    view_count = models.IntegerField(default=0, help_text="Number of views")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        ordering = ['-published_date', 'order']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def get_excerpt(self):
        """Return excerpt or first 200 chars of content"""
        if self.excerpt:
            return self.excerpt
        return self.content[:200] + "..." if len(self.content) > 200 else self.content

# Model to store Pricing section content
class PricingSection(models.Model):
    title = models.CharField(max_length=200, default="Our Packages & Rates")
    subtitle = models.CharField(max_length=300, default="NO HIDDEN FEES, CLEAR PRICING, EXCEPTIONAL SERVICE.")
    disclaimer = models.CharField(max_length=300, default="No hidden fees. Professional management you can count on.")
    cta_text = models.CharField(max_length=100, default="Request Management Pricing")
    cta_link = models.CharField(max_length=200, default="#contact")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pricing Section"
        verbose_name_plural = "Pricing Section"
    
    def __str__(self):
        return "Pricing Section"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Model to store Pricing Packages
class PricingPackage(models.Model):
    package_number = models.IntegerField(unique=True, help_text="Package number (1 or 2)")
    title = models.CharField(max_length=200, help_text="Package title (e.g., 'Rental Condominium Up to 2 Bedrooms')")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly price")
    services = models.TextField(help_text="Services included (one per line)")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['package_number']
        verbose_name = "Pricing Package"
        verbose_name_plural = "Pricing Packages"
    
    def __str__(self):
        return f"Package {self.package_number}: {self.title}"
    
    def get_services_list(self):
        """Return services as a list"""
        return [s.strip() for s in self.services.split('\n') if s.strip()]