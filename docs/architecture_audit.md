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

### Cart

Issue

Potential product_id / print_id mismatch.

Impact

Products may not be added correctly.

Priority

Critical

Status

To be verified.

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

### Framework and Application Configuration

- Django 5.2.6
Primary web framework used to implement:

        - URL routing
        - Views
        - Templates
        - Forms
        - Authentication
        - ORM and database access
        - Internationalisation

- django-extensions 4.1
Developer tooling used for project inspection and maintenance tasks.

- dj-database-url 3.0.1
Parses database connection strings from environment variables and deployment platforms.

---

### Database

- psycopg 3.2.10
PostgreSQL database adapter used by Django in local and production environments.

---

### Payments

- stripe 12.5.1
Provides:

        - Stripe Checkout Sessions
        - Payment processing
        - Payment verification
        - Webhook event handling
        
Used by:
        
        - shop/services/stripe.py
        - shop/services/webhooks.py

---

### Media Storage

- cloudinary 1.44.1
- cloudinary-storage
Cloud-based storage and delivery of product images.

- django-cloudinary-storage 0.3.0
Integrates Cloudinary with Django's file-storage system.

- django-storages 1.14.6

Provides configurable storage backends used by media and asset storage integrations.

--- 

### Static Files and Deployment

- whitenoise 6.11.0
Serves static assets in production environments.

- gunicorn 23.0.0
Production WSGI server used for deployment.

---

### Image Processing

- Pillow 11.3.0
Provides image processing functionality required by Django image fields.

### Environment Configuration

- python-decouple 3.8
Loads settings and secrets from environment variables.

- python-dotenv 1.1.1
Loads local environment variables during development.

---

## **Refactoring Risks**

### Overall Risk Assessment

The highest-risk areas of the Hearth Shop refactor are:

1. Stripe payment processing
2. Stripe webhook verification
3. Database models and migrations
4. Order creation and checkout
5. Authentication and permissions
6. Cloudinary media storage

These areas must be validated with automated and manual testing before and after any significant structural changes.

Lower-risk activities such as documentation updates, CSS cleanup, and navigation improvements may be completed throughout the project without substantial risk to business functionality.

### Risk Summary

- 🔴 High Risk: Stripe, Database, Orders
- 🟡 Medium Risk: Templates, Static Assets, Internationalisation
- 🟢 Low Risk: Documentation, CSS, Navigation

### Refactoring Risk Matrix


| Risk Area | Risk Level | Impact | Mitigation |
|------------|------------|---------|------------|
| Stripe Checkout Integration | 🔴 High | Customers may be unable to complete purchases if checkout sessions fail or redirect incorrectly. | Preserve existing checkout routes, verify Stripe configuration, and perform Stripe test transactions after each major change. |
| Stripe Webhook Processing | 🔴 High | Orders may not update correctly when payments succeed, fail, or are refunded. | Preserve webhook endpoints, verify webhook signatures, and test payment lifecycle events before deployment. |
| Database Models | 🔴 High | Product, order, or user data may become inaccessible if model relationships are altered incorrectly. | Backup the database before changes, document existing relationships, and verify model integrity after modifications. |
| Database Migrations | 🔴 High | Migration conflicts can break deployments or corrupt existing data. | Preserve migration history, test migrations locally, and never modify applied migrations without a clear rollback strategy. |
| Order Creation Logic | 🔴 High | Orders may contain incorrect information, totals, or payment statuses. | Create regression tests and verify complete checkout workflows after each refactor. |
| Cart Functionality | 🔴 High | Customers may be unable to add, update, or remove products from their cart. | Test add-to-cart, quantity updates, removal actions, and total calculations throughout development. |
| Authentication and Permissions | 🔴 High | Unauthorized access could expose user data or allow restricted actions. | Verify login, logout, registration, permissions, and staff-only functionality after changes. |
| Cloudinary Media Storage | 🔴 High | Product images may disappear or become inaccessible. | Preserve Cloudinary configuration and verify image uploads, retrieval, and display after modifications. |
| Order History | 🔴 High | Customers may lose access to historical purchase information. | Verify order ownership, permissions, and order-history functionality after changes. |
| Template Refactoring | 🟡 Medium | Pages may render incorrectly or links may fail due to broken template inheritance. | Refactor incrementally and test all major user journeys after template changes. |
| URL Refactoring | 🟡 Medium | Existing routes, redirects, or navigation links may stop working. | Preserve URL names and namespaces where possible, and test all existing routes. |
| Static Assets | 🟡 Medium | CSS, JavaScript, or images may fail to load, causing visual or functional issues. | Run collectstatic, verify asset loading locally and in production, and test responsive layouts. |
| Internationalisation (locale/) | 🟡 Medium | Translation files may become invalid or out of sync with templates. | Recompile locale files and verify translated pages after changes. |
| App Separation (US-15) | 🟡 Medium | Moving functionality into multiple apps may break imports, templates, or service references. | Extract functionality gradually and run regression tests after each structural change. |
| WhiteNoise Configuration | 🟡 Medium | Production static files may fail to load after deployment. | Verify static file serving in both local and deployed environments. |
| Documentation Updates | 🟢 Low | Documentation may become outdated during development. | Update documentation after each completed milestone. |
| README Maintenance | 🟢 Low | Installation or deployment instructions may become inaccurate. | Review documentation before each release. |
| CSS Cleanup | 🟢 Low | Minor visual inconsistencies may appear. | Compare layouts before and after changes and test across devices. |
| Navigation Refactoring | 🟢 Low | Menu links or page navigation may become inconsistent. | Manually verify all navigation paths after UI changes. |
| Template Naming Cleanup | 🟢 Low | Minor maintenance issues or broken references may occur. | Rename incrementally and verify template loading after each change. |

## Detailed Risk Analysis

### High Risk 🔴

#### Stripe Integration

Risk

Checkout and webhooks stop working.

Impact:
Customers may be unable to complete purchases or orders may not update payment status correctly.

Mitigation

- Create tests before refactoring.
- Verify Stripe test payments after each milestone.
- Preserve existing URL names and webhook routes

#### Database Models and Migrations

Risk

Changes to existing models may break migrations or cause data loss.

Impact:

Existing products, orders, or users could become inaccessible.

Mitigation

- Backup the database before schema changes.
- Preserve migration history.
- Test migrations in a staging environment before production deployment.


#### Order Processing

Risk

Orders created incorrectly.

Mitigation

Regression testing.

- Breaking migration history
- Breaking Stripe payment handling
- Breaking webhook processing
- Breaking order history

### Medium Risk 🟡

#### Templates

Risk

Broken URLs - Template inheritance changes

Impact:
Pages may render incorrectly.

Mitigation

Mitigation:
- Refactor incrementally.
- Verify page rendering after each change.
- Run manual testing of all key pages.

#### Static Assets

Risk:
Changes to static-file organisation may break stylesheets, JavaScript, or image references.

Impact:
Visual regressions or missing functionality.

Affected Areas:
- style.css
- main.js
- image paths

Mitigation:
- Run collectstatic tests.
- Verify asset loading locally and in production.

- Internationalisation updates: recompile locale files.

### Low Risk 🟢

README updates
User Stories
Project Workflow
Manual Testing Documentation
Automated Testing Documentation
CSS Cleanup
Navbar Refactoring
Template Naming Cleanup

---

## **Backup Strategy**
**Before refactoring:**

## Database

- Create PostgreSQL backup.
- Verify backup can be restored.

## Media

- Verify Cloudinary content exists.
- Export critical product images if needed.

## Source Code

- Commit current state.
- Push to GitHub.
- Tag stable release in Git.

## Migrations

- Review migration history.
- Store migration state before schema changes.

### Database Backup

Date
2026-10-23
Method
Django dumpdata
Result
Successful
Verification
Products, users, orders, and related records were confirmed present.
Backup Storage
Local backup storage outside the repository.

### Media Backup

Date
2026-10-23
Storage System
Cloudinary
Result
Successful
Verification
Product media confirmed available and representative samples exported.
Backup Storage
Local backup storage outside the repository.

### Source Code Backup

Method
Git tag
Tag
pre-refactor-baseline
Result
Successful
Purpose
Rollback point before structural refactoring.

---

## Dependency Audit Observations

### Actively Used

- Django
- Stripe
- Cloudinary
- django-cloudinary-storage
- django-storages
- Pillow
- WhiteNoise
- Gunicorn
- psycopg

### Requires Verification

- boto3
- botocore
- s3transfer

Reason:

AWS-related packages exist in requirements.txt but their current role in the project should be confirmed during the architecture audit.


