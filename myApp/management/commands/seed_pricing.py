from django.core.management.base import BaseCommand
from myApp.models import PricingSection, PricingPackage

class Command(BaseCommand):
    help = 'Seed pricing section with initial data'

    def handle(self, *args, **options):
        # Create or update Pricing Section
        pricing_section = PricingSection.get_instance()
        pricing_section.title = "Our Packages & Rates"
        pricing_section.subtitle = "NO HIDDEN FEES, CLEAR PRICING, EXCEPTIONAL SERVICE."
        pricing_section.disclaimer = "No hidden fees. Professional management you can count on."
        pricing_section.cta_text = "Request Management Pricing"
        pricing_section.cta_link = "#contact"
        pricing_section.save()
        self.stdout.write(self.style.SUCCESS(f'Updated: Pricing Section Header'))
        
        # Common services list for both packages
        services_list = """Marketing
In person Showing
Tenant Screening
Interim Inspection
Send Tax information
Move-in, Move-out inspections
Oversee from warranty claims
Oversee insurance claims
On Boarding
Monthly Statement
Move in Inspection Report
Background Check
Job Verification
20% Lease Renewal
75% Lease fee
Professional Pictures
Oversee all repairs during and after tenants move out"""
        
        # Package 1: Rental Condominium Up to 2 Bedrooms
        package1, created1 = PricingPackage.objects.get_or_create(
            package_number=1,
            defaults={
                'title': 'Rental Condominium Up to 2 Bedrooms',
                'price': 150.00,
                'services': services_list
            }
        )
        if not created1:
            package1.title = 'Rental Condominium Up to 2 Bedrooms'
            package1.price = 150.00
            package1.services = services_list
            package1.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created1 else "Updated"}: Package 1 - Rental Condominium Up to 2 Bedrooms - $150'))
        
        # Package 2: Single-Family Homes and Townhomes
        package2, created2 = PricingPackage.objects.get_or_create(
            package_number=2,
            defaults={
                'title': 'Single-Family Homes and Townhomes',
                'price': 225.00,
                'services': services_list
            }
        )
        if not created2:
            package2.title = 'Single-Family Homes and Townhomes'
            package2.price = 225.00
            package2.services = services_list
            package2.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created2 else "Updated"}: Package 2 - Single-Family Homes and Townhomes - $225'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully seeded pricing section!'))

