from django.shortcuts import render
from .image_helpers import get_all_section_images
from .models import (
    ServiceCard, ServicesSection, HeroSection, CredibilitySection, CredibilityCard,
    TestimonialsSection, Testimonial, StatisticsSection, PainPointsSection,
    MethodologySection, MethodologyStep, AboutSection, MissionVisionSection,
    LeadMagnetSection, FinalCTASection
)

def home(request):
    # Get all section images from database
    section_images = get_all_section_images()
    
    # Get all content sections from database
    hero_section = HeroSection.get_instance()
    credibility_section = CredibilitySection.get_instance()
    credibility_cards = CredibilityCard.objects.all().order_by('card_number')
    testimonials_section = TestimonialsSection.get_instance()
    testimonials = Testimonial.objects.all().order_by('testimonial_number')
    statistics_section = StatisticsSection.get_instance()
    pain_points_section = PainPointsSection.get_instance()
    services_section = ServicesSection.get_instance()
    service_cards = ServiceCard.objects.all().order_by('card_number')
    methodology_section = MethodologySection.get_instance()
    methodology_steps = MethodologyStep.objects.all().order_by('step_number')
    about_section = AboutSection.get_instance()
    mission_vision_section = MissionVisionSection.get_instance()
    lead_magnet_section = LeadMagnetSection.get_instance()
    final_cta_section = FinalCTASection.get_instance()
    
    context = {
        'section_images': section_images,
        'hero_section': hero_section,
        'credibility_section': credibility_section,
        'credibility_cards': credibility_cards,
        'testimonials_section': testimonials_section,
        'testimonials': testimonials,
        'statistics_section': statistics_section,
        'pain_points_section': pain_points_section,
        'services_section': services_section,
        'service_cards': service_cards,
        'methodology_section': methodology_section,
        'methodology_steps': methodology_steps,
        'about_section': about_section,
        'mission_vision_section': mission_vision_section,
        'lead_magnet_section': lead_magnet_section,
        'final_cta_section': final_cta_section,
    }
    return render(request, 'myApp/home.html', context)