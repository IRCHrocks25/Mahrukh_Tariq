from django.shortcuts import render
from .image_helpers import get_all_section_images
from .models import ServiceCard, ServicesSection

def home(request):
    # Get all section images from database
    section_images = get_all_section_images()
    
    # Get services section data
    services_section = ServicesSection.get_instance()
    service_cards = ServiceCard.objects.all().order_by('card_number')
    
    context = {
        'section_images': section_images,
        'services_section': services_section,
        'service_cards': service_cards
    }
    return render(request, 'myApp/home.html', context)