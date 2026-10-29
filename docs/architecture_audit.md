# Hearth Shop — Architecture Audit and Refactoring Plan


Hearth Shop is an existing Django e-commerce application for browsing and purchasing prints.

---

## **Project Overview**

Hearth Shop is a Django e-commerce application for selling photography prints and illustrations.

The current implementation uses:

- Django
- PostgreSQL
- Stripe
- Cloudinary
- Supabase
- Heroku

---

## Existing Structure

### Core Project

- hearth_shop/
- shop/
- media/
- static/
- staticfiles/

### Storage

- storage_cloudinary.py
- storage_supabase.py
- storage_backups.py

### Services

- cart.py
- checkout.py
- stripe.py
- webhooks.py

### Templates

- Homepage
- Cart
- Order History
- Contact
- Checkout Success
- Checkout Cancel

### Authentication

Django authentication templates are present.

### Internationalisation

locale/ directory present.

---

## **Existing Functionality**

### Catalogue

Implemented

Features:

- Photography gallery
- Illustration gallery
- Theme filtering
- Product modal

### Cart

Implemented

Status:

- Recently repaired
- Uses Print model

### Checkout

Implemented

Technology:

- Stripe Checkout Session

### Orders

Implemented

Features:

- Order model
- Order item model
- Order history

### Payment Verification

Implemented

Technology:

- Stripe Webhooks

### Media Management

Cloudinary

### User Accounts

Django authentication.

---

## **Known Defects Identified During Audit**

### Stripe Configuration Risk

Issue:

Stripe keys can be accidentally reversed.

Observed:

STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY were configured incorrectly during deployment.

Impact:

Checkout fails.

Status:

Resolved.

---

### Static File Synchronisation

Issue:

Changes sometimes visible locally but not on Heroku.

Impact:

UI inconsistencies.

Status:

Requires deployment verification.

---

### Large Cart Images

Observed in deployed application.

Status:

Under investigation.

---

### Modal Price Display

Observed in deployed application.

Status:

Under investigation.

---

## **Dependency Inventory**
## Dependencies

### Framework

- Django

### Media

- cloudinary
- cloudinary-storage

### Storage

- django-storages

### Payments

- stripe

### Database

- psycopg

### Images

- Pillow

### Deployment

- gunicorn
- whitenoise

---

## **Refactoring Risks**

## Refactoring Risks

### High Risk

- Breaking migration history
- Breaking Stripe payment handling
- Breaking webhook processing
- Breaking order history

### Medium Risk

- Static file management
- Template inheritance changes
- Internationalisation updates

### Low Risk

- Documentation updates
- CSS restructuring

---

## Backup Strategy

Before refactoring:

- Backup PostgreSQL database.
- Backup Cloudinary media.
- Create Git branch.
- Verify migration state.
- Tag stable release in Git.