# HEARTH Shop

## A multilingual Django e-commerce application for selling photography prints and illustrations. 

The platform includes artwork browsing, theme-based filtering, shopping cart functionality, **Stripe**-powered payments, **Cloudinary** image hosting, **Supabase** document storage, and internationalization support.

---

## Table of Contents

  - [Project Goals](#project-goals)
  - [Business Model](#business-model)
  - [Target Audience](#target-audience)
  - [Value Proposition](#value-proposition)
  - [User Stories](#user-stories)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Core Data Model](#core-data-model)
  - [Artwork Classification](#artwork-classification)
  - [Installation](#installation)
  - [Cloudinary Setup](#cloudinary-setup)
  - [Supabase Storage Setup](#supabase-storage-setup)
  - [Stripe Setup](#stripe-setup)
  - [Heroku Deployment](#heroku-deployment)
  - [Internationalization](#internationalization)
  - [Testing](#testing)
  - [License](#license)

---

## Project Goals

HEARTH Shop was created to provide artists with a dedicated platform for presenting, organizing, and selling original artwork online.

The project combines artwork management, cloud-based media delivery, secure payment processing, and multilingual support into a single e-commerce solution designed for both local and international audiences.

The platform prioritizes:

- Visual presentation of artwork
- Simple and intuitive browsing
- Efficient inventory management
- Secure online payments
- Scalable cloud storage
- International accessibility

Future development may include digital downloads, limited-edition collections, artist collaborations, and print-on-demand integration.

---

## Business Model

HEARTH Shop follows a direct-to-consumer (D2C) e-commerce model focused on the sale of original photography and illustration prints.

Revenue is generated through:

- Physical print sales
- Limited stock artwork collections
- Curated themed collections
- Potential future commissioned artwork services

The platform enables the artist to manage pricing, inventory, themes, and product presentation while maintaining full ownership and control over the catalog.

Potential future revenue streams include:

- Limited editions
- Seasonal collections
- Exclusive releases
- Digital artwork downloads
- Commissioned artwork
- Artist partnerships

---

## Target Audience

HEARTH Shop is designed for:

### Art Enthusiasts

Customers seeking original photography and illustration prints for personal collections.

### Home Decor Buyers

Individuals looking for artwork to decorate:

- Living rooms
- Bedrooms
- Offices
- Creative workspaces

### Gift Buyers

Customers searching for meaningful and visually distinctive gifts.

### International Customers

Visitors who benefit from multilingual navigation and purchasing experiences.

### Interior Designers and Small Galleries

Professionals sourcing artwork for styling, exhibitions, staging projects, and interior design concepts.

---

## Value Proposition

HEARTH Shop combines:

- Curated artwork collections
- Theme-based artwork discovery
- Secure online purchasing
- International accessibility
- Professional media delivery through Cloudinary
- Reliable cloud storage infrastructure
- Inventory and order management

The platform provides customers with an engaging shopping experience while giving administrators full control over catalog organization, pricing, stock, and content management.

## USER STORIES

### Customer
As a customer, I can:

  - Browse available prints and artwork collections.
  - View artwork details including title, image and price.
  - Filter artwork by theme and medium.
  - Add items to a shopping cart.
  - Complete purchases through Stripe Checkout.
  - View previous orders from my account.
  - Switch between supported languages.

## Shop Administrator
### As a shop administrator, I can:

  - Create and manage prints.
  - Upload artwork images and supporting documents
  - Assign themes and categories.
  - Manage pricing and stock levels.
  - Activate or deactivate artwork listings.
  - Review customer contact submissions.
  - Monitor orders and payment activity.
---

## Features
### Artwork Management. **Prints : Illustrations, Photography**
   
 Manage photography and illustration prints through a centralized `Print` model.
  - Artwork titles and descriptions
  - Pricing and stock management
  - Theme assignment
  - Category assignment
  - Active/inactive visibility control

## Photography & Illustration Galleries
### Browse artwork by type using dedicated gallery views.

  - Photography gallery
  - Illustration gallery
  - Modal image preview
  - Pagination
  - Theme filtering


## **Themes & Categories**
### Artwork organization is handled through two classification layers:

### Themes
Describe the subject of an artwork:

- Nature
- Animals
- Architecture
- Family
- Abstract

### Categories
Organize website content:

- Print
- Blog
- Info

## Cloudinary Image Hosting

Cloudinary is used for:
- Print images
- Category images
- Theme icons
  
## **Neon-DB Storage Integration**  

  Uses `django-storages` with Neon-DB endpoint for:
  - Manuals
  - Documents
  - Backup files

- **Stripe Checkout**  
  Secure payment flow with Stripe Checkout Sessions.

## **Shopping  Cart & Orders**  
 
 Features include:
  - Persistent cart storage
  - Order creation
  - Order history
  - Stripe integration

## **Multilingual Support**  
  Templates use `{% trans %}` and `{% blocktrans %}` for i18n.
```django
{% trans %}
{% blocktrans %}
```

- **Reusable Templates**  
  Shared `_gallery_grid.html` and `_pagination.html` snippets, plus `base_gallery.html`.

---

## Project Structure

```text
# Project Structure

```text
hearth_design/
│
├── manage.py
├── Procfile
├── README.md
├── requirements.txt
├── .gitignore
├── .python-version
├── .env
│
├── docs/
├── media/
├── static/
├── staticfiles/
├── hearth_shop/
├── shop/
└── hvenv/
```

<details>
<summary><strong>📁 docs</strong></summary>

```text
docs/
├── user_stories.md
├── project_workflow.md
├── manual_testing.md
└── automated_testing.md
```

</details>

<details>
<summary><strong>📁 media</strong></summary>

```text
media/
└── prints/
    ├── 1003/
    └── 2025/
```

</details>

<details>
<summary><strong>📁 static</strong></summary>

```text
static/
└── placeholder.txt
```

</details>

<details>
<summary><strong>📁 staticfiles</strong></summary>

```text
staticfiles/
├── admin/
│   ├── css/
│   ├── images/
│   └── js/
│
├── cloudinary/
│   ├── html/
│   └── js/
│
├── django_extensions/
├── css/
│   └── style.css
│
├── js/
├── images/
├── favicon.ico
└── placeholder.txt
```

</details>

<details>
<summary><strong>📁 hearth_shop (Django Project)</strong></summary>

```text
hearth_shop/
├── __init__.py
├── settings.py
├── urls.py
├── asgi.py
├── wsgi.py
├── __pycache__/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   ├── images/
│   │   ├── android-chrome-192x192.png
│   │   ├── favicon-32x32.png
│   │   └── ...
│   │
│   ├── sounds/
│   ├── favicon.ico
│   └── site.webmanifest
│
└── templates/
    ├── base.html
    │
    └── includes/
        └── navbar.html
```

</details>

<details>
<summary><strong>📁 shop (Django Application)</strong></summary>

```text
shop/
├── __init__.py
├── admin.py
├── apps.py
├── context_processor.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── views.py
│
├── storage_cloudinary.py
├── storage_supabase.py
├── storage_backups.py
│
├── __pycache__/
├── locale/
├── migrations/
│
├── management/
│   └── commands/
│       └── migrate_images_to_print.py
│
├── services/
│   ├── cart.py
│   ├── checkout.py
│   ├── stripe.py
│   └── webhooks.py
│
└── templates/
    │
    ├── registration/
    │   ├── login.html
    │   ├── signup.html
    │   ├── logged_out.html
    │   ├── password_change_form.html
    │   ├── password_change_done.html
    │   ├── password_reset.html
    │   ├── password_reset_done.html
    │   ├── password_reset_confirm.html
    │   ├── password_reset_complete.html
    │   └── password_reset_email.html
    │
    └── shop/
        ├── homepage.html
        ├── illustration_gallery.html
        ├── photography_gallery.html
        ├── themed_gallery.html
        ├── cart.html
        ├── order_history.html
        ├── contact.html
        ├── thank_you.html
        ├── upload.html
        ├── payment_success.html
        ├── checkout_thanks.html
        ├── payment_cancel.html
        └── _pagination.html
```

</details>

<details>
<summary><strong>📁 hvenv</strong></summary>

```text
hvenv/
├── include/
├── Lib/
├── Scripts/
└── pyvenv.cfg
```

</details>
```
> The placeholder file exists only to ensure Git tracks the static directory structure.

---

## Core Data Model

```
hearth_design/
├── docs/
├── hearth_shop/ ← Django project package
├── shop/            ← Django application
├── media/
├── static/
├── manage.py
├── README.md
├── Procfile
└── requirements.txt
```

```text
Category
    └── Organises site content (Print, Blog, Info)

Theme
    └── Describes artwork subjects
        (Nature, Animals, Architecture, etc.)

Print
    ├── title
    ├── slug
    ├── type (photo | illustration)
    ├── image
    ├── description
    ├── price
    ├── stock
    ├── themes
    ├── category
    └── is_active

Cart
    └── CartItem
            └── Print

Order
    └── OrderItem
            └── Print
```
---
## Artwork classification

### Print.type
Defines the artistic medium:
  - `photo`
  - `illustration`

### Theme
Defines the artwork subject:

  - Nature
  - Animals
  - Architecture
  - Family
  - Abstract

### Category
Defines the subject of a section:
- Artworks (Prints)
- Blog (future development)

## Single Source of Truth
The `Print` model acts as the single source of truth for:

- Title
- Description
- Image
- Price
- Stock
- Themes
- Artwork Metadata
---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hearthdesign/hearth_design.git
cd hearth-shop
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### Requirements include:

- Django
- Pillow
- stripe
- cloudinary
- cloudinary-storage
- django-storages
- psycopg
- python-dotenv

---

### 3. Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your_django_secret
DEBUG=True

## Database
DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db.<project>.supabase.co
DB_PORT=5432

## Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

## Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
```
---

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

---

## Cloudinary Setup

Cloudinary is used to store and deliver all public-facing images.

### Create a Cloudinary Account

1. Create an account at https://cloudinary.com
2. Open the Cloudinary Dashboard.
3. Obtain:

- Cloud Name
- API Key
- API Secret

### Add Credentials to `.env`

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

Cloudinary handles:

  - Print images
  - Category images
  - Theme icons

---

## NEON-DB Storage Setup

NEON-DB is used for document and backup storage.

1. Go to NEON-DB Dashboard 

2. Navigate to
→ Storage → Configuration → S3.

3. Generate:
  - Access Key ID 
  - Secret Access Key.

4. Create a bucket (e.g. media) and set it to Public (for images visibility)


5. Add credentials to .env.

NEON-DB stores:

  - Manuals
  - Documents
  - Backup files

---

## Stripe Setup

1. Create a Stripe account.

2. Obtain:
  - Publishable Key (pk_...)
  - Secret Key (sk_...)

1. Add them to .env as:
```env
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
```

> **Important:** Do not reverse the keys.
> - Secret keys begin with `sk_`
> - Publishable keys begin with `pk_`

Update `success_url` and `cancel_url` to match your deployment domain.



## Heroku Deployment

### Login and Create Application
```bash
heroku login
heroku create
```

### Deploy
```bash
git push heroku main
```

### Configure environment variables:
```bash
heroku config:set SECRET_KEY=...

heroku config:set CLOUDINARY_CLOUD_NAME=...
heroku config:set CLOUDINARY_API_KEY=...
heroku config:set CLOUDINARY_API_SECRET=...

heroku config:set STRIPE_SECRET_KEY=...
heroku config:set STRIPE_PUBLISHABLE_KEY=...
```

### Apply migrations:
```bash
heroku run python manage.py migrate
```

### Collect static files:
```bash
heroku run python manage.py collectstatic --noinput
```

### Verify deployment:
Open the Application

```bash
heroku open
```

---

## Internationalization

The application supports multiple languages using Django's built-in translation framework.

### In the Templates 
Translations are implemented using:

```django
{% trans %}
{% blocktrans %}
```

### Configure languages in settings.py:

```python
USE_I18N = True
LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('fr', 'Français'),
    ...
]
```

---

# Manual Testing

## Gallery

| Test | Expected Result | Pass |
|--------|--------|--------|
| Open gallery page | Gallery loads correctly | ✅ |
| Open modal | Larger image opens | ✅ |
| Change language | Language changes | ✅ |
| Add to cart | Product added correctly | ✅ |

### Reusable Templates
_gallery_grid.html → renders thumbnails. 
_pagination.html → renders pagination links.
base_gallery.html → includes both in blocks for reuse.

Specialized templates (homepage.html, illustration_gallery.html, photography_gallery.html, themed_gallery.html) extend base_gallery.

## Testing Locally

### Artwork Upload
  - Upload a print through Django Admin or the upload form.
  - Verify that images are stored in Cloudinary.

### Gallery Views

- Browse photography and illustration galleries.
- Test pagination.
- Test theme filtering.

### Shopping Experience

- Add items to the cart.
![alt text](docs\readme\image-12.png)

- Update quantities.
![alt text](docs\readme\image-13.png)
![alt text](docs\readme\image-14.png)
![alt text](docs\readme\image-15.png)

- Remove items.
![alt text](docs\readme\image-16.png)

### Checkout

- Complete a Stripe test transaction.
![alt text](docs\readme\image-17.png)
![alt text](docs\readme\image-18.png)
![alt text](docs\readme\image-19.png)

- Verify order creation.
![alt text](docs\readme\image-20.png)

- Confirm order history functionality.
![alt text](docs\readme\image-21.png)

- Payment Cancelled
![alt text](docs\readme\image-11.png)

---

# Automated Testing

## Django Tests

Run:
python manage.py test

Result:
All tests passed successfully.

---

# Validation Testing

## HTML Validation

All pages were validated using the W3C HTML Validator.
Minor warnings were reviewed and deemed acceptable where applicable.

## CSS Validation

The stylesheet was tested using the W3C CSS Validator.

Result:

- 0 CSS errors
- Remaining warnings relate to browser-supported vendor extensions and intentional styling choices.

Validator:
https://jigsaw.w3.org/css-validator/

![CSS Validation](assets/testing/css-validator.webp)

---

## JSHint results

Result

Metrics

There are 23 functions in this file.
Function with the largest signature take 4 arguments, while the median is 0.
Largest function has 15 statements in it, while the median is 4.
The most complex function has a cyclomatic complexity value of 6 while the median is 2.

---

## Lighthouse

![alt text](docs\readme\image.png)

![alt text](docs\readme\image-1.png)

![alt text](docs\readme\image-2.png)

![alt text](docs\readme\image-7.png)

![alt text](docs\readme\image-8.png)

![alt text](docs\readme\image-6.png)

### Passed audits (21)

- Use efficient cache lifetimes
- Layout shift culprits
- Optimize DOM size
- Duplicated JavaScript
- Font display
- Forced reflow
- INP breakdown
- LCP request discovery
- Legacy JavaScript
- Modern HTTP
- Optimize viewport for mobile
- Minify CSS
- Reduce unused CSS
- Reduce unused JavaScript
- Avoids enormous network payloads Total size was 200 KiB
- User Timing marks and measures
- JavaScript execution time 0.1 s
- Minimizes main-thread work 0.6 s
- Avoid non-composited animations
- Image elements have explicit width and height
- Page didn't prevent back/forward cache restoration


![alt text](docs\readme\image-9.png)

Passed audits (21)

- [aria-*] attributes match their roles
- [aria-hidden="true"] is not present on the document <body>
- [aria-*] attributes have valid values
- [aria-*] attributes are valid and not misspelled
- Image elements have [alt] attributes
- [user-scalable="no"] is not used in the <meta name="viewport"> element and the [maximum-scale] attribute is not less than 5.
- Select elements have associated label elements.
- ARIA attributes are used as specified for the element's role
- [aria-hidden="true"] elements do not contain focusable descendents
- Elements use only permitted ARIA attributes
- Background and foreground colors have a sufficient contrast ratio
- Document has a <title> element
- <html> element has a [lang] attribute
- <html> element has a valid value for its [lang] attribute
- Links have a discernible name
- Lists contain only <li> elements and script supporting elements (<script> and <template>).
- List items (<li>) are contained within <ul>, <ol> or <menu> parent elements
- Touch targets have sufficient size and spacing.
- Heading elements appear in a sequentially-descending order
- Document has a main landmark.
- Elements with role="none" or role="presentation" do not have conflicts

![alt text](docs\readme\image-10.png)

Passed audits (13)

- Uses HTTPS
- Avoids deprecated APIs
- Avoids third-party cookies
- Allows users to paste into input fields
- Avoids requesting the geolocation permission on page load
- Avoids requesting the notification permission on page load
- Displays images with correct aspect ratio
- Serves images with appropriate resolution
- Page has the HTML doctype
- Properly defines charset
- No browser errors logged to the console
- No issues in the Issues panel in Chrome Devtools
- Page has valid source maps


![alt text](docs\readme\image-22.png)

Passed audits (8)

- Page isn’t blocked from indexing
- Document has a <title> element
- Document has a meta description
- Page has successful HTTP status code
- Links have descriptive text
- Links are crawlable
- Image elements have [alt] attributes
- Document has a valid hreflang

---

### HTTPS Testing

The application enforces HTTPS in production using Django security settings:

- SECURE_SSL_REDIRECT
- SECURE_PROXY_SSL_HEADER
- Secure session cookies
- Secure CSRF cookies

Testing confirmed that HTTP requests are automatically redirected to HTTPS.

---

## PEP8 tested with **Ruff** (`charliermarsh.ruff`) extension 

```python
ruff check .
```

### After running the first test the following problems have been found:

### 1. Unused variable created:
```python
cart, created = Cart.objects.get_or_create(
user=request.user
)
```

Has been changed to:
```python
cart, _ = Cart.objects.get_or_create(
user=request.user
)
```

### 2. Unused variable event:
```python
event, status_code = handle_stripe_webhook(
payload,
sig_header
)
```

Has been changed to:
```python
_event, status_code = handle_stripe_webhook(
payload,
sig_header
)
```

### 3. Translation warning (INT001):
```Python
message = _(
f"Hi {form.cleaned_data['name']},\n\n"
"Thank you for reaching out..."
)
```
Wrong for Django i18n.

Has been replaced with:

```python
message = _(
"Hi %(name)s,\n\n"
"Thank you for reaching out to us. "
"We've received your message and will get back to you shortly.\n\n"
"Best regards,\n"
"Hearth Design Team"
) % {
"name": form.cleaned_data["name"]
}
```

### 4, Variable name change:

The variable "created" has been replaced with "_created"

### After executing the test (ruff check .)

Result:
All checks passed!

---

## Project Documentation

Additional documentation is available in the `docs/` directory:

docs/
├── user_stories.md
├── project_workflow.md
├── automated_testing.md
└── manual_testing.md

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

