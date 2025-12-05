from django.shortcuts import render
from .image_helpers import get_all_section_images

def home(request):
    # Get all section images from database
    section_images = get_all_section_images()
    
    context = {
        'section_images': section_images
    }
    return render(request, 'myApp/home.html', context)