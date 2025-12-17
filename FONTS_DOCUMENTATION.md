# Font Usage Documentation

## Current Font Configuration

The website uses **two Google Fonts**:

### 1. **Raleway** (Headlines/Display)
- **Type:** Sans-serif
- **Weights:** 400, 500, 600, 700, 800
- **Usage:** Headlines, titles, navigation, and all display text
- **Recommended Weights:** 500-700 for premium feel
- **Google Fonts Link:** https://fonts.google.com/specimen/Raleway

### 2. **Plus Jakarta Sans** (Body Text)
- **Type:** Sans-serif
- **Weights:** 300, 400, 500, 600
- **Usage:** Body text, paragraphs, and general content
- **Recommended Weights:** 300-500 for airy, modern feel
- **Google Fonts Link:** https://fonts.google.com/specimen/Plus+Jakarta+Sans

---

## Font Configuration Location

**File:** `myApp/templates/myApp/base.html`

### Google Fonts Import (Lines 14-17)
```html
<!-- Google Fonts: Raleway (headlines) + Plus Jakarta Sans (body) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
```

### Tailwind CSS Configuration (Lines 30-34)
```javascript
fontFamily: {
    'display': ['Raleway', 'sans-serif'],
    'sans': ['Plus Jakarta Sans', 'sans-serif'],
}
```

### CSS Styles (Lines 44-52)
```css
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 300;
    letter-spacing: 0.01em;
}
p, li, a, button, input, textarea {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Raleway', sans-serif;
    letter-spacing: 0.01em;
}
```

---

## Font Usage Throughout the Website

### **Raleway** (Display Font) - Used For:

#### 1. **Navigation/Header**
- **File:** `myApp/templates/myApp/partials/header.html`
- **Location:** Desktop navigation menu (line 12) - uses `font-display` class
- **Location:** Mobile menu (line 24) - uses `font-display` class
- **Elements:** All navigation links (Services, Testimonials, Method, About, Contact)
- **Note:** No inline font styles - uses Tailwind `font-display` class

#### 2. **All Headings (h1, h2, h3, h4, h5, h6)**
- **Applied globally** via CSS in `base.html`
- **Class:** `font-display` (Tailwind utility class)

#### 3. **Hero Section**
- **File:** `myApp/templates/myApp/partials/hero.html`
- **Element:** Main headline (h1) - "Stop Losing Money to Property Managers Who Don't Care." (line 8)

#### 4. **Statistics Section**
- **File:** `myApp/templates/myApp/partials/statistics.html`
- **Elements:**
  - Section title (h3) - "Numbers that reflect systems — not luck." (line 18)
  - All statistic numbers (150+, 100+, 94%, 4.9) (lines 38, 63, 88, 113)

#### 5. **Credibility Section**
- **File:** `myApp/templates/myApp/partials/credibility.html`
- **Elements:**
  - Main title (h2) - "Proven Experience. Personal Commitment. Real Results." (line 25)
  - Subtitle (h3) - "Why Landlords Choose Garden Gate" (line 46)
  - Card titles (h4) (lines 73, 96)

#### 6. **Services Section**
- **File:** `myApp/templates/myApp/partials/services.html`
- **Elements:**
  - Section title (h2) (line 5)
  - Service card titles (h3) (line 27)

#### 7. **Testimonials Section**
- **File:** `myApp/templates/myApp/partials/testimonials.html`
- **Element:** Section title (h2) (line 5)

#### 8. **Methodology Section**
- **File:** `myApp/templates/myApp/partials/methodology.html`
- **Elements:**
  - Section title (h2) (line 5)
  - Step titles (h3) (lines 44, 58)

#### 9. **Pain Points Section**
- **File:** `myApp/templates/myApp/partials/pain_points.html`
- **Elements:**
  - Section title (h2) (line 5)
  - Subsection titles (h3) (lines 19, 52)

#### 10. **About Section**
- **File:** `myApp/templates/myApp/partials/about.html`
- **Element:** Section title (h2) (line 11)

#### 11. **Mission & Vision Section**
- **File:** `myApp/templates/myApp/partials/mission_vision.html`
- **Elements:**
  - Main title (h2) - "Built for landlords who expect clarity, control, and calm." (line 18)
  - Mission subtitle (h3) (line 50)
  - Vision subtitle (h3) (line 81)

#### 12. **Lead Magnet Section**
- **File:** `myApp/templates/myApp/partials/lead_magnet.html`
- **Element:** Section title (h2) (line 13)

#### 13. **Final CTA Section**
- **File:** `myApp/templates/myApp/partials/final_cta.html`
- **Element:** Section title (h2) (line 8)

#### 14. **Footer**
- **File:** `myApp/templates/myApp/partials/footer.html`
- **Element:** Company name (h3) (line 8)

---

### **Plus Jakarta Sans** (Body Font) - Used For:

#### 1. **All Body Text**
- **Applied globally** via CSS in `base.html` (line 45)
- **Default font** for all paragraphs, descriptions, and body content
- **Default weight:** 300 (light) for airy, premium feel

#### 2. **Hero Section**
- **File:** `myApp/templates/myApp/partials/hero.html`
- **Elements:**
  - Subtitle paragraph (line 15)
  - Description paragraph (line 18)
  - Button text (line 21)

#### 3. **All Section Descriptions**
- Used in all partial templates for:
  - Paragraph text
  - Description text
  - Card descriptions
  - Body content

#### 4. **Statistics Section**
- **File:** `myApp/templates/myApp/partials/statistics.html`
- **Elements:**
  - Statistic labels ("Properties / Units Managed", "Satisfied Landlords", etc.)
  - Description text below statistics

#### 5. **Credibility Section**
- **File:** `myApp/templates/myApp/partials/credibility.html`
- **Elements:**
  - Section description (line 28)
  - Card descriptions (lines 77, 100)

#### 6. **All Other Sections**
- All paragraph text, descriptions, and body content throughout the website uses Lora by default

---

## Font Class Usage

### Tailwind CSS Classes:
- **`font-display`** → Applies Raleway font (for headlines, titles, navigation)
- **`font-sans`** → Applies Plus Jakarta Sans font (for body text)
- **No inline font styles** → All fonts applied via classes or global CSS

### Font Weight Guidelines:
- **Body paragraphs:** `font-light` (300) or no class (defaults to 300)
- **Headings:** `font-semibold` (600) or `font-bold` (700)
- **Buttons:** `font-semibold` (600)
- **Navigation:** `font-medium` (500)

---

## Summary

- **Raleway** = All headlines, titles, navigation, and display text (weights 500-700)
- **Plus Jakarta Sans** = All body text, paragraphs, descriptions, and general content (weights 300-500)

The font pairing creates a premium, modern design:
- **Raleway** provides structured, upscale, geometric headlines
- **Plus Jakarta Sans** provides airy, modern, and expensive-feeling body text when used light

---

## Notes

- All headings (h1-h6) automatically use Raleway via CSS with 0.01em letter-spacing
- All body text automatically uses Plus Jakarta Sans via CSS with font-weight 300
- The `font-display` Tailwind class is used throughout templates to explicitly apply Raleway
- Navigation menu uses `font-display` class (no inline styles)
- Letter-spacing reduced from 0.02em to 0.01em for more premium, less template-ish feel
- Font weights optimized: Body (300-400), Headings (600-700), Buttons (600)

