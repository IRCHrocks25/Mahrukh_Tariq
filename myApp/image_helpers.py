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
    return {section.section_name: {
        'image_url': section.image_url or '',
        'image_alt': section.image_alt or '',
        'icon_url': section.icon_url or '',
        'background_image_url': section.background_image_url or '',
    } for section in sections}

