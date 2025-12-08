from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import SectionImage, MediaAsset, ServiceCard, ServicesSection
from .utils.cloudinary_utils import upload_to_cloudinary
import json

# Login view
def dashboard_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            return render(request, 'myApp/dashboard/login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'myApp/dashboard/login.html')

# Logout view
@login_required
def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')

# Dashboard home
@login_required
def dashboard_index(request):
    # Get all sections except methodology icons and header logo (we'll show them separately)
    sections = SectionImage.objects.exclude(section_name__startswith='methodology_icon_').exclude(section_name='header_logo')
    # Get logo separately to show it first
    logo = SectionImage.objects.filter(section_name='header_logo').first()
    return render(request, 'myApp/dashboard/index.html', {
        'sections': sections,
        'logo': logo
    })

# Edit section images
@login_required
def section_image_edit(request, section_id):
    section = get_object_or_404(SectionImage, id=section_id)
    
    if request.method == 'POST':
        # Only update the fields that are relevant to this section type
        if 'background' in section.section_name:
            section.background_image_url = request.POST.get('background_image_url', '')
        elif 'icon' in section.section_name:
            section.icon_url = request.POST.get('icon_url', '')
        else:
            section.image_url = request.POST.get('image_url', '')
            section.image_alt = request.POST.get('image_alt', '')
        section.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/section_edit.html', {
        'section': section
    })

# Image upload endpoint
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        image_file = request.FILES['image']
        folder = request.POST.get('folder', 'garden_gate')
        
        # Upload to Cloudinary
        result = upload_to_cloudinary(image_file, folder=folder)
        
        # Save to database
        media_asset = MediaAsset.objects.create(
            url=result['url'],
            secure_url=result['secure_url'],
            public_id=result['public_id'],
            folder=folder,
            filename=image_file.name,
            alt_text=request.POST.get('alt_text', '')
        )
        
        return JsonResponse({
            'success': True,
            'url': result['secure_url'],
            'web_url': result['web_url'],
            'thumb_url': result['thumb_url'],
            'public_id': result['public_id'],
            'id': media_asset.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Edit all methodology icons at once
@login_required
def methodology_icons_edit(request):
    # Get all 5 methodology icon sections
    icons = {}
    icon_names = ['Assessment', 'Protection', 'Management', 'Communication', 'Optimization']
    
    for i in range(1, 6):
        try:
            section = SectionImage.objects.get(section_name=f'methodology_icon_{i}')
            icons[i] = section
        except SectionImage.DoesNotExist:
            # Create if doesn't exist
            section = SectionImage.objects.create(
                section_name=f'methodology_icon_{i}',
                display_name=f'Methodology - Icon {i} ({icon_names[i-1]})'
            )
            icons[i] = section
    
    if request.method == 'POST':
        # Update all icons
        for i in range(1, 6):
            icon_url = request.POST.get(f'icon_{i}_url', '')
            icon_alt = request.POST.get(f'icon_{i}_alt', '')
            icons[i].icon_url = icon_url
            icons[i].image_alt = icon_alt
            icons[i].save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/methodology_icons_edit.html', {
        'icons': icons
    })

# Gallery view
@login_required
def gallery(request):
    assets = MediaAsset.objects.all()
    
    # If AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        assets_data = [{
            'id': asset.id,
            'url': asset.secure_url,
            'thumb_url': asset.secure_url.replace('/upload/', '/upload/f_webp,q_80,w_400/'),
            'filename': asset.filename or asset.public_id,
            'alt_text': asset.alt_text
        } for asset in assets]
        return JsonResponse({'assets': assets_data})
    
    return render(request, 'myApp/dashboard/gallery.html', {
        'assets': assets
    })

# Edit services section
@login_required
def services_edit(request):
    # Get or create services section header
    services_section = ServicesSection.get_instance()
    
    # Get or create service cards
    cards = {}
    for i in range(1, 4):
        card, created = ServiceCard.objects.get_or_create(
            card_number=i,
            defaults={
                'title': f'Service {i}',
                'subtitle': '',
                'features': '',
                'result_text': '',
                'cta_text': 'Learn More',
                'cta_link': '#consultation'
            }
        )
        cards[i] = card
    
    if request.method == 'POST':
        # Update section header
        services_section.title = request.POST.get('section_title', '')
        services_section.description = request.POST.get('section_description', '')
        services_section.cta_text = request.POST.get('section_cta_text', 'Find Your Fit')
        services_section.cta_link = request.POST.get('section_cta_link', '#consultation')
        services_section.save()
        
        # Update each card
        for i in range(1, 4):
            card = cards[i]
            card.title = request.POST.get(f'card_{i}_title', '')
            card.subtitle = request.POST.get(f'card_{i}_subtitle', '')
            card.image_url = request.POST.get(f'card_{i}_image_url', '')
            card.image_alt = request.POST.get(f'card_{i}_image_alt', '')
            card.features = request.POST.get(f'card_{i}_features', '')
            card.result_text = request.POST.get(f'card_{i}_result_text', '')
            card.cta_text = request.POST.get(f'card_{i}_cta_text', 'Learn More')
            card.cta_link = request.POST.get(f'card_{i}_cta_link', '#consultation')
            card.save()
        
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/services_edit.html', {
        'services_section': services_section,
        'cards': cards
    })

