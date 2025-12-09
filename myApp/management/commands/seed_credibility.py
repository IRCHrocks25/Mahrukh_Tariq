from django.core.management.base import BaseCommand
from myApp.models import CredibilitySection, CredibilityCard

class Command(BaseCommand):
    help = 'Seed credibility section with initial data'

    def handle(self, *args, **options):
        # Create or update Credibility Section Header
        credibility_section = CredibilitySection.get_instance()
        credibility_section.title = "Proven Experience. Personal Commitment.<br>Real Results."
        credibility_section.description = "Garden Gate is not a franchise or volume-driven agency. It's a boutique property management firm built on 13 years of hands-on real estate experience — backed by a personal portfolio that proves its systems deliver results."
        credibility_section.subtitle = "Why Landlords Choose Garden Gate"
        credibility_section.subtitle_description = "Most property managers have never been landlords. Mahrukh Tariq is both. Here's why that matters to your bottom line:"
        credibility_section.save()
        self.stdout.write(self.style.SUCCESS(f'Updated: Credibility Section Header'))
        
        # Credibility Card 1: Personal Tenant Screening
        card1, created1 = CredibilityCard.objects.get_or_create(
            card_number=1,
            defaults={
                'title': 'Personal Tenant Screening',
                'description': 'With an average 4-day placement time, vacancies are filled faster than competitors who sit empty for weeks. Experience as a landlord ensures speed without compromising quality.'
            }
        )
        if not created1:
            card1.title = 'Personal Tenant Screening'
            card1.description = 'With an average 4-day placement time, vacancies are filled faster than competitors who sit empty for weeks. Experience as a landlord ensures speed without compromising quality.'
            card1.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created1 else "Updated"}: Credibility Card 1 - Personal Tenant Screening'))
        
        # Credibility Card 2: Real Repair Costs, Not Markups
        card2, created2 = CredibilityCard.objects.get_or_create(
            card_number=2,
            defaults={
                'title': 'Real Repair Costs, Not Markups',
                'description': "Garden Gate's trusted contractors also maintain Mahrukh's own units, which means no unnecessary add-ons or inflated pricing. While many managers allow vendors to tack on up to 25% markups, Garden Gate clients pay the same fair rates she pays herself."
            }
        )
        if not created2:
            card2.title = 'Real Repair Costs, Not Markups'
            card2.description = "Garden Gate's trusted contractors also maintain Mahrukh's own units, which means no unnecessary add-ons or inflated pricing. While many managers allow vendors to tack on up to 25% markups, Garden Gate clients pay the same fair rates she pays herself."
            card2.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created2 else "Updated"}: Credibility Card 2 - Real Repair Costs, Not Markups'))
        
        # Credibility Card 3: Direct Access, No Call Centers
        card3, created3 = CredibilityCard.objects.get_or_create(
            card_number=3,
            defaults={
                'title': 'Direct Access, No Call Centers',
                'description': "Clients communicate directly with the decision-maker managing their property, not a rotating staff member or automated system."
            }
        )
        if not created3:
            card3.title = 'Direct Access, No Call Centers'
            card3.description = "Clients communicate directly with the decision-maker managing their property, not a rotating staff member or automated system."
            card3.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created3 else "Updated"}: Credibility Card 3 - Direct Access, No Call Centers'))
        
        # Credibility Card 4: Proven Systems Backed by 90 Units
        card4, created4 = CredibilityCard.objects.get_or_create(
            card_number=4,
            defaults={
                'title': 'Proven Systems Backed by 90 Units',
                'description': "Every process at Garden Gate is field-tested through the management of Mahrukh's own 90-unit portfolio, ensuring efficiency, reliability, and real-world results."
            }
        )
        if not created4:
            card4.title = 'Proven Systems Backed by 90 Units'
            card4.description = "Every process at Garden Gate is field-tested through the management of Mahrukh's own 90-unit portfolio, ensuring efficiency, reliability, and real-world results."
            card4.save()
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created4 else "Updated"}: Credibility Card 4 - Proven Systems Backed by 90 Units'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully seeded credibility section!'))

