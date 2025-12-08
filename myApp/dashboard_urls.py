from django.urls import path
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    path('login/', dashboard_views.dashboard_login, name='login'),
    path('logout/', dashboard_views.dashboard_logout, name='logout'),
    path('', dashboard_views.dashboard_index, name='index'),
    path('gallery/', dashboard_views.gallery, name='gallery'),
    path('upload-image/', dashboard_views.upload_image, name='upload_image'),
    path('methodology-icons/', dashboard_views.methodology_icons_edit, name='methodology_icons_edit'),
    path('services/', dashboard_views.services_edit, name='services_edit'),
    path('section/<int:section_id>/edit/', dashboard_views.section_image_edit, name='section_edit'),
]

