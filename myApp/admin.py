from django.contrib import admin
from .models import SectionImage, MediaAsset

@admin.register(SectionImage)
class SectionImageAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'section_name', 'has_image', 'has_icon', 'has_background', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['display_name', 'section_name']
    readonly_fields = ['updated_at']
    
    def has_image(self, obj):
        return bool(obj.image_url)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def has_icon(self, obj):
        return bool(obj.icon_url)
    has_icon.boolean = True
    has_icon.short_description = 'Has Icon'
    
    def has_background(self, obj):
        return bool(obj.background_image_url)
    has_background.boolean = True
    has_background.short_description = 'Has Background'

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'folder', 'uploaded_at']
    list_filter = ['folder', 'uploaded_at']
    search_fields = ['filename', 'public_id', 'alt_text']
    readonly_fields = ['url', 'secure_url', 'public_id', 'uploaded_at']
