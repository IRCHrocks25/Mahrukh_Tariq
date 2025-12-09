from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
from .models import (
    SectionImage, MediaAsset, ServiceCard, ServicesSection,
    HeroSection, CredibilitySection, CredibilityCard,
    TestimonialsSection, Testimonial, StatisticsSection,
    PainPointsSection, MethodologySection, MethodologyStep,
    AboutSection, MissionVisionSection, LeadMagnetSection, FinalCTASection
)
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

# Edit Hero section
@login_required
def hero_edit(request):
    hero = HeroSection.get_instance()
    
    if request.method == 'POST':
        hero.title = request.POST.get('title', '')
        hero.subtitle = request.POST.get('subtitle', '')
        hero.description = request.POST.get('description', '')
        hero.cta_text = request.POST.get('cta_text', 'Show Me How This Actually Works')
        hero.cta_link = request.POST.get('cta_link', '#consultation')
        hero.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/hero_edit.html', {
        'hero': hero
    })

# Edit Credibility section
@login_required
def credibility_edit(request):
    credibility = CredibilitySection.get_instance()
    
    # Get or create credibility cards
    cards = {}
    for i in range(1, 5):
        card, created = CredibilityCard.objects.get_or_create(
            card_number=i,
            defaults={
                'title': f'Value Point {i}',
                'description': ''
            }
        )
        cards[i] = card
    
    if request.method == 'POST':
        credibility.title = request.POST.get('title', '')
        credibility.description = request.POST.get('description', '')
        credibility.subtitle = request.POST.get('subtitle', '')
        credibility.subtitle_description = request.POST.get('subtitle_description', '')
        credibility.save()
        
        # Update cards
        for i in range(1, 5):
            card = cards[i]
            card.title = request.POST.get(f'card_{i}_title', '')
            card.description = request.POST.get(f'card_{i}_description', '')
            card.save()
        
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/credibility_edit.html', {
        'credibility': credibility,
        'cards': cards
    })

# Edit Testimonials section
@login_required
def testimonials_edit(request):
    testimonials_section = TestimonialsSection.get_instance()
    testimonials = Testimonial.objects.all().order_by('testimonial_number')
    
    if request.method == 'POST':
        testimonials_section.title = request.POST.get('title', '')
        testimonials_section.cta_text = request.POST.get('cta_text', 'See What We Can Do')
        testimonials_section.cta_link = request.POST.get('cta_link', '#consultation')
        testimonials_section.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/testimonials_edit.html', {
        'testimonials_section': testimonials_section,
        'testimonials': testimonials
    })

# Edit individual testimonial
@login_required
def testimonial_edit(request, testimonial_id=None):
    if testimonial_id:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    else:
        # Create new testimonial
        max_number = Testimonial.objects.aggregate(models.Max('testimonial_number'))['testimonial_number__max'] or 0
        testimonial = Testimonial.objects.create(testimonial_number=max_number + 1)
    
    if request.method == 'POST':
        testimonial.avatar_url = request.POST.get('avatar_url', '')
        testimonial.avatar_alt = request.POST.get('avatar_alt', '')
        testimonial.quote_short = request.POST.get('quote_short', '')
        testimonial.quote_long = request.POST.get('quote_long', '')
        testimonial.author_name = request.POST.get('author_name', '')
        testimonial.author_title = request.POST.get('author_title', '')
        testimonial.save()
        return redirect('dashboard:testimonials_edit')
    
    return render(request, 'myApp/dashboard/testimonial_edit.html', {
        'testimonial': testimonial
    })

# Edit Statistics section
@login_required
def statistics_edit(request):
    statistics = StatisticsSection.get_instance()
    
    if request.method == 'POST':
        statistics.title = request.POST.get('title', '')
        statistics.subtitle = request.POST.get('subtitle', '')
        statistics.point_1 = request.POST.get('point_1', '')
        statistics.point_2 = request.POST.get('point_2', '')
        statistics.point_3 = request.POST.get('point_3', '')
        statistics.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/statistics_edit.html', {
        'statistics': statistics
    })

# Edit Pain Points section
@login_required
def pain_points_edit(request):
    pain_points = PainPointsSection.get_instance()
    
    if request.method == 'POST':
        pain_points.title = request.POST.get('title', '')
        pain_points.description = request.POST.get('description', '')
        pain_points.pain_point_1 = request.POST.get('pain_point_1', '')
        pain_points.pain_point_2 = request.POST.get('pain_point_2', '')
        pain_points.pain_point_3 = request.POST.get('pain_point_3', '')
        pain_points.pain_point_4 = request.POST.get('pain_point_4', '')
        pain_points.pain_point_5 = request.POST.get('pain_point_5', '')
        pain_points.solution_1 = request.POST.get('solution_1', '')
        pain_points.solution_2 = request.POST.get('solution_2', '')
        pain_points.solution_3 = request.POST.get('solution_3', '')
        pain_points.solution_4 = request.POST.get('solution_4', '')
        pain_points.solution_5 = request.POST.get('solution_5', '')
        pain_points.cta_text = request.POST.get('cta_text', 'Turn Frustrations Into Results')
        pain_points.cta_link = request.POST.get('cta_link', '#consultation')
        pain_points.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/pain_points_edit.html', {
        'pain_points': pain_points
    })

# Edit Methodology section
@login_required
def methodology_edit(request):
    methodology = MethodologySection.get_instance()
    steps = MethodologyStep.objects.all().order_by('step_number')
    
    if request.method == 'POST':
        methodology.title = request.POST.get('title', '')
        methodology.description = request.POST.get('description', '')
        methodology.cta_text = request.POST.get('cta_text', 'See the Framework in Action')
        methodology.cta_link = request.POST.get('cta_link', '#consultation')
        methodology.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/methodology_edit.html', {
        'methodology': methodology,
        'steps': steps
    })

# Edit Methodology step
@login_required
def methodology_step_edit(request, step_id=None):
    if step_id:
        step = get_object_or_404(MethodologyStep, id=step_id)
    else:
        max_number = MethodologyStep.objects.aggregate(models.Max('step_number'))['step_number__max'] or 0
        step = MethodologyStep.objects.create(step_number=max_number + 1)
    
    if request.method == 'POST':
        if step_id:  # Only allow updating step_number for new steps
            step.title = request.POST.get('title', '')
            step.description = request.POST.get('description', '')
            step.result_text = request.POST.get('result_text', '')
        else:  # New step - can set step_number
            step_number = request.POST.get('step_number')
            if step_number:
                try:
                    step.step_number = int(step_number)
                except ValueError:
                    pass
            step.title = request.POST.get('title', '')
            step.description = request.POST.get('description', '')
            step.result_text = request.POST.get('result_text', '')
        step.save()
        return redirect('dashboard:methodology_edit')
    
    return render(request, 'myApp/dashboard/methodology_step_edit.html', {
        'step': step
    })

# Edit About section
@login_required
def about_edit(request):
    about = AboutSection.get_instance()
    
    if request.method == 'POST':
        about.title = request.POST.get('title', '')
        about.content = request.POST.get('content', '')
        about.quote_text = request.POST.get('quote_text', '')
        about.quote_author = request.POST.get('quote_author', '')
        about.cta_text = request.POST.get('cta_text', "See If We're a Fit")
        about.cta_link = request.POST.get('cta_link', '#consultation')
        about.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/about_edit.html', {
        'about': about
    })

# Edit Mission/Vision section
@login_required
def mission_vision_edit(request):
    mission_vision = MissionVisionSection.get_instance()
    
    if request.method == 'POST':
        mission_vision.mission_title = request.POST.get('mission_title', '')
        mission_vision.mission_subtitle = request.POST.get('mission_subtitle', '')
        mission_vision.mission_description = request.POST.get('mission_description', '')
        mission_vision.vision_title = request.POST.get('vision_title', '')
        mission_vision.vision_subtitle = request.POST.get('vision_subtitle', '')
        mission_vision.vision_description = request.POST.get('vision_description', '')
        mission_vision.cta_text = request.POST.get('cta_text', 'Join Us')
        mission_vision.cta_link = request.POST.get('cta_link', '#consultation')
        mission_vision.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/mission_vision_edit.html', {
        'mission_vision': mission_vision
    })

# Edit Lead Magnet section
@login_required
def lead_magnet_edit(request):
    lead_magnet = LeadMagnetSection.get_instance()
    
    if request.method == 'POST':
        lead_magnet.title = request.POST.get('title', '')
        lead_magnet.subtitle = request.POST.get('subtitle', '')
        lead_magnet.bullet_1 = request.POST.get('bullet_1', '')
        lead_magnet.bullet_2 = request.POST.get('bullet_2', '')
        lead_magnet.bullet_3 = request.POST.get('bullet_3', '')
        lead_magnet.description = request.POST.get('description', '')
        lead_magnet.cta_text = request.POST.get('cta_text', 'Show Me How This Actually Works')
        lead_magnet.cta_link = request.POST.get('cta_link', '#consultation')
        lead_magnet.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/lead_magnet_edit.html', {
        'lead_magnet': lead_magnet
    })

# Edit Final CTA section
@login_required
def final_cta_edit(request):
    final_cta = FinalCTASection.get_instance()
    
    if request.method == 'POST':
        final_cta.title = request.POST.get('title', '')
        final_cta.description = request.POST.get('description', '')
        final_cta.cta_text = request.POST.get('cta_text', 'Show Me How This Actually Works')
        final_cta.cta_link = request.POST.get('cta_link', '#contact')
        final_cta.save()
        return redirect('dashboard:index')
    
    return render(request, 'myApp/dashboard/final_cta_edit.html', {
        'final_cta': final_cta
    })

