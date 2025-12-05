# Image Dashboard Setup Guide

This is a simplified dashboard system that allows you to edit **only images, icons, and background images** for your website sections.

## 🚀 Quick Start

### 1. Install Dependencies

The required packages are already in `requirements.txt`. Make sure you have:
- `cloudinary==1.43.0`
- `pillow==10.4.0`
- `python-dotenv==1.0.1`

### 2. Set Up Cloudinary

1. Sign up for a free account at [cloudinary.com](https://cloudinary.com)
2. Get your credentials from the dashboard
3. Create a `.env` file in the project root:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Important:** Add `.env` to `.gitignore` to keep credentials secure!

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Initialize Sections

This creates all the section entries in the database:

```bash
python manage.py init_sections
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Access Dashboard

1. Run the server: `python manage.py runserver`
2. Go to: `http://localhost:8000/dashboard/`
3. Log in with your superuser credentials

## 📸 How to Use

### Editing Images

1. Go to **Dashboard** → Click on any section (e.g., "Hero Section - Background Image")
2. You'll see three fields:
   - **Image URL**: For regular images
   - **Icon URL**: For icons (like methodology icons)
   - **Background Image URL**: For background images
3. Click **"Choose from Gallery"** to:
   - Browse previously uploaded images
   - Upload new images
4. Enter **Alt Text** for accessibility
5. Click **Save Changes**

### Uploading Images

1. Go to **Gallery** in the sidebar
2. Upload images using the form
3. Images are automatically:
   - Compressed for web
   - Converted to WebP format
   - Stored in Cloudinary CDN
4. Copy image URLs to use in sections

### Image Picker Modal

Every image field has a **"Choose from Gallery"** button that opens a modal with:
- **Gallery Tab**: Browse and select from uploaded images
- **Upload Tab**: Upload new images (supports multiple images at once)

## 📋 Available Sections

The system includes these editable sections:

- **Hero Section**
  - Background Image
  - Main Image (if needed)

- **About Section**
  - Background Image

- **Statistics Section**
  - Background Image

- **Methodology Section**
  - Icon 1 (Assessment)
  - Icon 2 (Protection)
  - Icon 3 (Management)
  - Icon 4 (Communication)
  - Icon 5 (Optimization)

- **Lead Magnet Section**
  - Tablet Image

- **Final CTA Section**
  - Background Image

## 🔧 How It Works

1. **Database Storage**: All image URLs are stored in the `SectionImage` model
2. **Cloudinary Integration**: Images are uploaded to Cloudinary CDN for fast delivery
3. **Template Integration**: Templates automatically pull image URLs from the database
4. **Fallback**: If no image is set, templates show placeholder text

## 🎨 Customization

### Adding New Sections

1. Add a new entry to `init_sections.py`:
```python
{'section_name': 'new_section', 'display_name': 'New Section - Image'},
```

2. Run the init command again:
```bash
python manage.py init_sections
```

3. Update your template to use the image:
```django
<img src="{{ section_images.new_section.image_url|default:'placeholder.jpg' }}" alt="...">
```

### Changing Cloudinary Folder

Edit the default folder in:
- `dashboard_views.py` (upload_image function)
- `utils/cloudinary_utils.py` (upload_to_cloudinary function)

## 🔒 Security

- Dashboard requires login (superuser account)
- All views are protected with `@login_required`
- CSRF protection enabled
- Environment variables for sensitive data

## 📝 Notes

- **Only images are editable** - All text content remains in templates
- Images are automatically optimized for web
- All images are stored in Cloudinary (no local storage)
- Gallery shows all uploaded images across all sections

## 🐛 Troubleshooting

### Images Not Uploading

1. Check `.env` file has correct Cloudinary credentials
2. Verify Cloudinary account is active
3. Check file size (max 10MB, auto-compressed)

### Images Not Showing

1. Check image URLs are saved in dashboard
2. Verify Cloudinary images are public
3. Check browser console for errors

### Can't Access Dashboard

1. Make sure you created a superuser
2. Check you're logged in
3. Verify `LOGIN_URL` is set correctly in `settings.py`

## 📚 Files Structure

```
myApp/
├── models.py                    # SectionImage, MediaAsset models
├── dashboard_views.py            # Dashboard views
├── dashboard_urls.py            # Dashboard URLs
├── image_helpers.py              # Helper functions
├── utils/
│   └── cloudinary_utils.py      # Cloudinary upload/compression
├── management/
│   └── commands/
│       └── init_sections.py     # Initialize sections
└── templates/
    └── myApp/
        └── dashboard/           # Dashboard templates
            ├── base.html
            ├── login.html
            ├── index.html
            ├── section_edit.html
            ├── gallery.html
            └── image_picker_modal.html
```

## ✅ Checklist

- [ ] Cloudinary account created
- [ ] `.env` file configured
- [ ] Migrations run
- [ ] Sections initialized
- [ ] Superuser created
- [ ] Dashboard accessible
- [ ] Test image upload
- [ ] Test image selection
- [ ] Verify images show on website

---

**That's it!** You now have a simple dashboard to manage all images on your website without touching code. 🎉

