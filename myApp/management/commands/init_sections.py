from django.core.management.base import BaseCommand
from myApp.models import SectionImage

class Command(BaseCommand):
    help = 'Initialize section images for all website sections'

    def handle(self, *args, **options):
        sections = [
            {'section_name': 'header_logo', 'display_name': 'Header - Logo'},
            {'section_name': 'hero_background', 'display_name': 'Hero Section - Background Image'},
            {'section_name': 'hero_image', 'display_name': 'Hero Section - Main Image'},
            {'section_name': 'about_image', 'display_name': 'About Section - Image'},
            {'section_name': 'about_background', 'display_name': 'About Section - Background Image'},
            {'section_name': 'statistics_background', 'display_name': 'Statistics Section - Background Image'},
            {'section_name': 'methodology_icon_1', 'display_name': 'Methodology - Icon 1 (Assessment)'},
            {'section_name': 'methodology_icon_2', 'display_name': 'Methodology - Icon 2 (Protection)'},
            {'section_name': 'methodology_icon_3', 'display_name': 'Methodology - Icon 3 (Management)'},
            {'section_name': 'methodology_icon_4', 'display_name': 'Methodology - Icon 4 (Communication)'},
            {'section_name': 'methodology_icon_5', 'display_name': 'Methodology - Icon 5 (Optimization)'},
            {'section_name': 'lead_magnet_tablet', 'display_name': 'Lead Magnet - Tablet Image'},
            {'section_name': 'final_cta_background', 'display_name': 'Final CTA - Background Image'},
        ]
        
        created_count = 0
        for section_data in sections:
            section, created = SectionImage.objects.get_or_create(
                section_name=section_data['section_name'],
                defaults={'display_name': section_data['display_name']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {section.display_name}'))
            else:
                self.stdout.write(f'Skipped (already exists): {section.display_name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully initialized {created_count} new sections.'))

