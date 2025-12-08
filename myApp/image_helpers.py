from .models import SectionImage

def get_section_image(section_name):
    """Get image URLs for a specific section"""
    try:
        section = SectionImage.objects.get(section_name=section_name)
        return {
            'image_url': section.image_url or '',
            'image_alt': section.image_alt or '',
            'icon_url': section.icon_url or '',
            'background_image_url': section.background_image_url or '',
        }
    except SectionImage.DoesNotExist:
        return {
            'image_url': '',
            'image_alt': '',
            'icon_url': '',
            'background_image_url': '',
        }

def get_all_section_images():
    """Get all section images as a dictionary"""
    sections = SectionImage.objects.all()
    result = {section.section_name: {
        'image_url': section.image_url or '',
        'image_alt': section.image_alt or '',
        'icon_url': section.icon_url or '',
        'background_image_url': section.background_image_url or '',
    } for section in sections}
    
    # Ensure expected sections exist (even if empty) to prevent template errors
    expected_sections = ['hero_background', 'hero_image', 'about_background', 'statistics_background']
    for section_name in expected_sections:
        if section_name not in result:
            result[section_name] = {
                'image_url': '',
                'image_alt': '',
                'icon_url': '',
                'background_image_url': '',
            }
    
    return result

