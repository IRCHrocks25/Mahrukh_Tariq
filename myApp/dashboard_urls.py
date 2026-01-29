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
    # Content section edits
    path('hero/', dashboard_views.hero_edit, name='hero_edit'),
    path('credibility/', dashboard_views.credibility_edit, name='credibility_edit'),
    path('testimonials/', dashboard_views.testimonials_edit, name='testimonials_edit'),
    path('testimonial/<int:testimonial_id>/edit/', dashboard_views.testimonial_edit, name='testimonial_edit'),
    path('testimonial/new/', dashboard_views.testimonial_edit, name='testimonial_new'),
    path('statistics/', dashboard_views.statistics_edit, name='statistics_edit'),
    path('pain-points/', dashboard_views.pain_points_edit, name='pain_points_edit'),
    path('methodology/', dashboard_views.methodology_edit, name='methodology_edit'),
    path('methodology-step/<int:step_id>/edit/', dashboard_views.methodology_step_edit, name='methodology_step_edit'),
    path('methodology-step/new/', dashboard_views.methodology_step_edit, name='methodology_step_new'),
    path('about/', dashboard_views.about_edit, name='about_edit'),
    path('mission-vision/', dashboard_views.mission_vision_edit, name='mission_vision_edit'),
    path('lead-magnet/', dashboard_views.lead_magnet_edit, name='lead_magnet_edit'),
    path('final-cta/', dashboard_views.final_cta_edit, name='final_cta_edit'),
    path('blog/', dashboard_views.blog_edit, name='blog_edit'),
    path('blog-post/<int:post_id>/edit/', dashboard_views.blog_post_edit, name='blog_post_edit'),
    path('blog-post/new/', dashboard_views.blog_post_edit, name='blog_post_new'),
]

