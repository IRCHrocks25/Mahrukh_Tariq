from django.core.management.base import BaseCommand
from myApp.models import ServicesSection, ServiceCard

class Command(BaseCommand):
    help = 'Seed services section with initial data'

    def handle(self, *args, **options):
        # Create or update Services Section
        services_section = ServicesSection.get_instance()
        services_section.title = "Management That Fits Your Goals."
        services_section.description = "Every landlord is different. Some want complete freedom. Others prefer involvement. We tailor our service to fit you."
        services_section.cta_text = "Find Out If We're the Right Fit"
        services_section.cta_link = "#consultation"
        services_section.save()
        self.stdout.write(self.style.SUCCESS(f'Updated: Services Section Header'))
        
        # Service Card 1: Full-Service Management
        card1, created1 = ServiceCard.objects.get_or_create(
            card_number=1,
            defaults={
                'title': 'Full-Service Management',
                'subtitle': 'For landlords who want zero hassle.',
                'image_url': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop&q=80',
                'image_alt': 'Full-Service Property Management',
                'features': 'Tenant placement and screening\nLease management and rent collection\n24/7 maintenance coordination\nFinancial reporting and inspections',
                'result_text': 'Result: Steady income, no stress, full trust.',
                'cta_text': 'Get a Free Rental Analysis',
                'cta_link': '#consultation'
            }
        )
        if not created1:
            card1.title = 'Full-Service Management'
            card1.subtitle = 'For landlords who want zero hassle.'
            card1.image_url = 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop&q=80'
            card1.image_alt = 'Full-Service Property Management'
            card1.features = 'Tenant placement and screening\nLease management and rent collection\n24/7 maintenance coordination\nFinancial reporting and inspections'
            card1.result_text = 'Result: Steady income, no stress, full trust.'
            card1.cta_text = 'Get a Free Rental Analysis'
            card1.cta_link = '#consultation'
            card1.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created1 else "Updated"}: Service Card 1 - Full-Service Management'))
        
        # Service Card 2: Tenant Placement Only
        card2, created2 = ServiceCard.objects.get_or_create(
            card_number=2,
            defaults={
                'title': 'Tenant Placement Only',
                'subtitle': "We'll find your tenant — you take it from there.",
                'image_url': 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400&h=300&fit=crop&q=80',
                'image_alt': 'Tenant Placement',
                'features': 'Professional marketing and showings\nThorough pre-qualification and screening\nLease prep and move-in coordination',
                'result_text': 'Result: Quality tenants, fast occupancy.',
                'cta_text': 'Get a Free Rental Analysis',
                'cta_link': '#consultation'
            }
        )
        if not created2:
            card2.title = 'Tenant Placement Only'
            card2.subtitle = "We'll find your tenant — you take it from there."
            card2.image_url = 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400&h=300&fit=crop&q=80'
            card2.image_alt = 'Tenant Placement'
            card2.features = 'Professional marketing and showings\nThorough pre-qualification and screening\nLease prep and move-in coordination'
            card2.result_text = 'Result: Quality tenants, fast occupancy.'
            card2.cta_text = 'Get a Free Rental Analysis'
            card2.cta_link = '#consultation'
            card2.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created2 else "Updated"}: Service Card 2 - Tenant Placement Only'))
        
        # Service Card 3: Portfolio Building & Investment Guidance
        card3, created3 = ServiceCard.objects.get_or_create(
            card_number=3,
            defaults={
                'title': 'Portfolio Building & Investment Guidance',
                'subtitle': 'For investors growing wealth long-term.',
                'image_url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=300&fit=crop&q=80',
                'image_alt': 'Portfolio Building',
                'features': 'Market analysis and property selection\nFinancing and acquisition support\nPost-purchase management and optimization',
                'result_text': 'Result: Profitable portfolios built with strategy and care.',
                'cta_text': 'Get a Free Rental Analysis',
                'cta_link': '#consultation'
            }
        )
        if not created3:
            card3.title = 'Portfolio Building & Investment Guidance'
            card3.subtitle = 'For investors growing wealth long-term.'
            card3.image_url = 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=300&fit=crop&q=80'
            card3.image_alt = 'Portfolio Building'
            card3.features = 'Market analysis and property selection\nFinancing and acquisition support\nPost-purchase management and optimization'
            card3.result_text = 'Result: Profitable portfolios built with strategy and care.'
            card3.cta_text = 'Get a Free Rental Analysis'
            card3.cta_link = '#consultation'
            card3.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created3 else "Updated"}: Service Card 3 - Portfolio Building & Investment Guidance'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully seeded services section!'))

