# Hearth Shop — User Stories and Refactoring Plan


## Table of Contents

### Project Information
1. [Project Context](#1-project-context)
2. [Priority Legend](#2-priority-legend)
3. [User Stories](#3-user-stories)

### Must Have (M)
- [US-01 Audit and Preserve the Existing Application](#us-01--audit-and-preserve-the-existing-application-m)
- [US-02 Browse the Product Catalogue](#us-02--browse-the-product-catalogue-m)
- [US-03 Fix Add-to-Cart Functionality](#us-03--fix-add-to-cart-functionality-m)
- [US-04 Complete Checkout and Create Orders](#us-04--complete-checkout-and-create-orders-m)
- [US-05 Fix Stripe Redirects and Checkout Feedback](#us-05--fix-stripe-redirects-and-checkout-feedback-m)
- [US-06 Verify Payments and Update Order Status](#us-06--verify-payments-and-update-order-status-m)
- [US-07 View Order History Securely](#us-07--view-order-history-securely-m)
- [US-08 Improve Authentication and Authorization](#us-08--improve-authentication-and-authorization-m)

### Should Have (S)
- [US-09 Implement Frontend Product CRUD](#us-09--implement-frontend-product-crud-s)
- [US-10 Send Transactional Order Emails](#us-10--send-transactional-order-emails-s)
- [US-12 Improve Contact Form Functionality](#us-12--improve-contact-form-functionality-s)
- [US-13 Improve Accessibility and Responsive Design](#us-13--improve-accessibility-and-responsive-design-s)
- [US-14 Implement SEO and Error Handling](#us-14--implement-seo-and-error-handling-s)
- [US-15 Refactor Into Reusable Django Apps Safely](#us-15--refactor-into-reusable-django-apps-safely-s)
- [US-18 Improve Testing and Deployment Documentation](#us-18--improve-testing-and-deployment-documentation-s)

### Could Have (C)
- [US-11 Add a Dedicated Newsletter Signup](#us-11--add-a-dedicated-newsletter-signup-c)
- [US-16 Document the Business Model, Database Schema, and Design](#us-16--document-the-business-model-database-schema-and-design-c)
- [US-17 Document the Marketing Strategy and Facebook Evidence](#us-17--document-the-marketing-strategy-and-facebook-evidence-c)

## Future Enhancements
- [Future Commerce Features](#future-commerce-features)
- [Future Customer Features](#future-customer-features)
- [Future Product Features](#future-product-features)
- [Future Marketing Features](#future-marketing-features)
- [Future Technical Improvements](#future-technical-improvements)


## 1. Project context

Hearth Shop is an existing Django e-commerce application for browsing and purchasing prints.

The current project includes:

- `hearth_shop/` — Django project configuration, settings, and root URL configuration.
- `shop/` — the existing Django app, including models, views, forms, migrations, services, management commands, templates, and translations.
- `media/prints/` — product media.
- `static/` and `hearth_shop/static/` — existing static asset directories whose roles are to be confirmed.
- `staticfiles/` — collected static files, subject to confirmation of the current configuration.
- `manage.py`, `Procfile`, `requirements.txt`, and `README.md` — project and deployment files.

The project will first address existing functionality and data integrity before introducing structural changes. New Django apps may be introduced incrementally where they provide a clear separation of responsibilities.

The existing database, product media, model relationships, migration history, payment processing, and working functionality must be preserved during the refactoring process.

## 2. Priority legend

See ../docs/project_workflow.md

## 3. USER STORIES

### US-01 — Audit and preserve the existing application (M)

**Priority:** 🔴 Critical

**User story:** As a developer, I want to understand the existing application structure and dependencies so that I can improve the project without losing data or breaking working functionality.

**Acceptance criteria**

- [ ] Django settings, root URLs, app URLs, models, views, forms, and services are understood.
- [ ] Existing cart, checkout, Stripe, webhook, order, and order-history implementations are identified.
- [ ] Model relationships and migration history are reviewed.
- [ ] Source static assets, collected static files, and uploaded media are identified.
- [ ] The database and important product media are backed up before risky structural changes.
- [ ] Local-only files and secrets are excluded from version control.
- [ ] The initial application state and known defects are documented.
- [ ] Existing dependencies and potential refactoring risks are recorded.

**Current locations:** `hearth_shop/`, `shop/`, `media/`, `static/`, `staticfiles/`, and project configuration files.

### US-02 — Browse the product catalogue (M)

**Priority:** 🟡 High

**User story:** As a customer, I want to browse prints and view their details so that I can decide what to purchase.

**Acceptance criteria**

- [ ] Product listings display accurate names, descriptions, prices, and images.
- [ ] Product detail pages load correctly.
- [ ] Product information comes from the database.
- [ ] Missing or unavailable images are handled gracefully.
- [ ] Product links and navigation work correctly.
- [ ] Catalogue pages are usable on desktop, tablet, and mobile.
- [ ] Relevant automated tests pass.

### US-03 — Fix add-to-cart functionality (M)

**Priority:** 🔴 Critical

**User story:** As a customer, I want to add products to my cart and manage quantities so that I can prepare my purchase.

**Acceptance criteria**

- [ ] The mismatch between the submitted `product_id` and the view's expected `print_id` is resolved.
- [ ] A consistent product identifier is used throughout the cart form and processing logic.
- [ ] Valid products can be added to the cart.
- [ ] The cart displays the correct products and quantities.
- [ ] Customers can update quantities and remove items.
- [ ] Cart totals use trusted database prices rather than submitted prices.
- [ ] Invalid product identifiers and quantities are handled safely.
- [ ] An empty cart displays a useful message and a route back to browsing.
- [ ] Automated tests cover adding, updating, removing, and invalid input.
- [ ] Manual testing confirms that cart operations work through the website.

### US-04 — Complete checkout and create orders (M)

**Priority:** 🔴 Critical

**User story:** As a customer, I want checkout to create an order containing the correct items and totals so that my purchase can be processed and tracked.

**Acceptance criteria**

- [ ] Checkout displays the correct cart contents, quantities, and total.
- [ ] The server recalculates prices and totals using trusted data.
- [ ] An order and associated order items are created correctly.
- [ ] Order items preserve relevant product details, quantities, and purchase prices.
- [ ] Orders receive appropriate initial payment and fulfilment statuses.
- [ ] Failed or abandoned payments do not mark orders as paid.
- [ ] Repeated requests do not unintentionally create duplicate orders.
- [ ] Database relationships and order totals are validated.
- [ ] Automated tests cover order creation, invalid carts, and failure scenarios.

### US-05 — Fix Stripe redirects and checkout feedback (M)

**Priority:** 🔴 Critical

**User story:** As a customer, I want Stripe Checkout to return me to valid success or cancellation pages so that I understand the outcome of my checkout attempt.

**Acceptance criteria**

- [ ] Success and cancellation routes exist and resolve correctly.
- [ ] Hardcoded localhost redirect URLs are replaced with correctly configured application URLs.
- [ ] Django URL names and namespaces match those referenced by the checkout code.
- [ ] The success page communicates payment status accurately.
- [ ] A redirect to the success page alone does not establish that payment succeeded.
- [ ] The cancellation page provides a clear route back to the cart.
- [ ] Stripe configuration and secrets are read from environment variables.
- [ ] Payment errors are handled without exposing secrets or sensitive information.
- [ ] Automated tests cover checkout session creation and relevant errors.
- [ ] Production configuration uses the correct HTTPS domain and callback routes.

### US-06 — Verify payments and update order status (M)

**Priority:** 🔴 Critical

**User story:** As a customer, I want my payment to be verified by the server so that my order is marked paid only after payment has been confirmed.

**Acceptance criteria**

- [ ] A Stripe webhook endpoint is implemented or the existing endpoint is verified.
- [ ] Webhook signatures are verified using the configured Stripe webhook secret.
- [ ] Invalid webhook signatures are rejected.
- [ ] Only verified, relevant payment events can update an order's payment status.
- [ ] Repeated webhook events are handled idempotently.
- [ ] Unknown or unmatched orders are handled safely and logged appropriately.
- [ ] Pending, failed, cancelled, and successful payment states are handled consistently.
- [ ] Visiting a success URL cannot, by itself, mark an order as paid.
- [ ] Automated tests cover valid events, invalid signatures, unknown orders, and repeated events.
- [ ] Stripe test-mode payments and webhook delivery are verified before production use.

### US-07 — View order history securely (M)

**Priority:** 🔴 Critical

**User story:** As a signed-in customer, I want to see my previous orders and their statuses so that I can track my purchases.

**Acceptance criteria**

- [ ] Successfully created orders appear in the appropriate order history.
- [ ] Each order displays its reference, date, items, quantities, total, and status.
- [ ] Customers without orders see a useful empty state.
- [ ] Customers can view only their own orders.
- [ ] Direct URL access to another customer's order is denied.
- [ ] Unauthenticated access is redirected or denied appropriately.
- [ ] Automated tests cover order ownership and permissions.

### US-08 — Improve authentication and authorization (M)

**Priority:** 🔴 Critical

**User story:** As a customer, I want secure access to my account and orders so that my personal information remains private.

**Acceptance criteria**

- [ ] Registration, login, and logout work correctly.
- [ ] Signed-in users are redirected away from login or registration pages where appropriate.
- [ ] Protected actions require authentication.
- [ ] Customers cannot grant themselves staff or administrator privileges.
- [ ] Staff-only actions enforce server-side permissions.
- [ ] Direct URL requests cannot bypass authorization.
- [ ] Forms validate submitted data and protect state-changing requests against CSRF.
- [ ] Automated tests cover authenticated, unauthenticated, and unauthorized access.

### US-09 — Implement frontend product CRUD (S)

**Priority:** 🔴 Critical

**User story:** As an authorized staff member, I want to create, view, edit, and delete products through frontend forms so that product management does not depend exclusively on Django admin.

**Acceptance criteria**

- [ ] Authorized staff can create products using validated forms.
- [ ] Authorized staff can view and edit existing products.
- [ ] Authorized staff can delete products after confirmation.
- [ ] Required fields, prices, and uploaded images are validated.
- [ ] Ordinary customers cannot create, edit, or delete shared product records.
- [ ] Every operation checks permissions on the server.
- [ ] Direct URL requests cannot bypass permissions.
- [ ] State-changing forms use CSRF protection.
- [ ] Automated tests cover CRUD operations, validation, and unauthorized requests.
- [ ] Existing products and media remain intact during implementation.

### US-10 — Send transactional order emails (S)

**Priority:** 🟡 High

**User story:** As a customer, I want to receive confirmation after my payment is verified so that I have a record of my purchase.

**Acceptance criteria**

- [ ] Confirmation emails are triggered by verified payment outcomes.
- [ ] Emails include the order reference and relevant purchase details.
- [ ] Repeated webhook events do not unintentionally send duplicate confirmations.
- [ ] Email failures are logged and handled appropriately.
- [ ] HTML and plain-text email templates are available where appropriate.
- [ ] Email configuration is managed through environment variables.
- [ ] Automated tests verify the email trigger and content.

### US-11 — Add a dedicated newsletter signup (C)

**Priority:** 🟡 High

**User story:** As a visitor, I want to subscribe to a newsletter separately from the contact form so that I can choose to receive marketing updates.

**Acceptance criteria**

- [ ] A dedicated newsletter form is available on the website.
- [ ] Email addresses are validated and duplicate subscriptions are handled.
- [ ] Subscription consent and relevant records are stored appropriately.
- [ ] The privacy notice explains how subscription data is used.
- [ ] An appropriate unsubscribe process is implemented.
- [ ] Marketing messages are sent in accordance with applicable consent and privacy requirements.
- [ ] Automated tests cover signup, duplicate submissions, and consent handling.

### US-12 — Improve contact form functionality (S)

**Priority:** 🟡 High

**User story:** As a visitor, I want to send an enquiry through a working contact form so that I can ask questions about products or orders.

**Acceptance criteria**

- [ ] Required fields and email addresses are validated.
- [ ] Successful submissions display a clear confirmation.
- [ ] Invalid submissions display useful error messages.
- [ ] Enquiries are stored or delivered according to the documented design.
- [ ] Contact enquiries and newsletter subscriptions are handled separately.
- [ ] Appropriate spam protection and input validation are in place.
- [ ] Automated tests cover valid and invalid submissions.

### US-13 — Improve accessibility and responsive design (S)

**Priority:** 🟡 High

**User story:** As a visitor, I want an accessible and responsive interface so that I can use the shop on different devices and with different access needs.

**Acceptance criteria**

- [ ] Text and interactive elements have sufficient colour contrast.
- [ ] Forms have associated labels and understandable validation messages.
- [ ] Main interactions can be completed using a keyboard.
- [ ] Images have appropriate alternative text.
- [ ] Links and buttons have clear, meaningful labels.
- [ ] Layouts work on mobile, tablet, and desktop.
- [ ] Cart and checkout provide clear success and error feedback.
- [ ] Placeholder images and static file references resolve correctly.
- [ ] Accessibility checks and results are documented.

### US-14 — Implement SEO and error handling (S)

**Priority:** 🟡 High

**User story:** As a visitor or search engine crawler, I want descriptive page metadata, a sitemap, and useful error pages so that the website is easier to discover and navigate.

**Acceptance criteria**

- [ ] The base template includes an appropriate meta description.
- [ ] Important pages can supply their own relevant metadata.
- [ ] A valid `robots.txt` endpoint is available.
- [ ] A sitemap includes appropriate public canonical URLs.
- [ ] Canonical links are configured where appropriate.
- [ ] External links use suitable `rel` attributes when required.
- [ ] A custom 404 page is configured and tested under production-like conditions.
- [ ] Production settings disable `DEBUG`.
- [ ] Checkout, payment, and order-history routes resolve correctly.
- [ ] Automated tests cover the sitemap, robots route, and relevant error handling.

### US-15 — Refactor into reusable Django apps safely (S)

**Priority:** 🟡 High

**User story:** As a developer, I want the application divided into clear, reusable Django apps so that the project is easier to maintain and extend.

**Acceptance criteria**

- [ ] Existing responsibilities, dependencies, and routes are documented before code is moved.
- [ ] The existing `shop` app remains functional during the refactor.
- [ ] App boundaries reflect actual responsibilities and avoid unnecessary complexity.
- [ ] Catalogue, cart, orders, payments, accounts, and other responsibilities are separated where appropriate.
- [ ] New apps have correct configuration and are registered in `INSTALLED_APPS`.
- [ ] Imports, URL names and namespaces, templates, static references, and settings are updated.
- [ ] Existing model relationships and migration history are preserved.
- [ ] Database backups and migration checks are completed before risky model changes.
- [ ] Tests pass after each meaningful refactoring step.
- [ ] Existing functionality is checked for regressions after changes.
- [ ] Deployment configuration is updated if externally used routes or settings change.

### Planned App Structure

The current shop app may be incrementally separated into reusable apps where doing so improves maintainability and separation of concerns.
Potential app boundaries include:

- accounts/
- catalog/
- cart/
- orders/
- payments/
- notifications/
- contact/
- marketing/
- pages/

Only apps that provide a clear separation of responsibilities will be created.
Existing functionality, migrations, media, and database relationships must remain intact during the refactor.

### US-16 — Document the business model, database schema, and design (C)

**Priority:** 🟢 Supporting

**User story:** As an assessor or developer, I want the business purpose, target audience, database relationships, and design decisions documented so that I can understand the application and its rationale.

**Acceptance criteria**

- [ ] The business model and value proposition are explained.
- [ ] The target audience and customer needs are justified.
- [ ] The implemented database schema and model relationships are documented.
- [ ] An ER diagram reflects the actual schema.
- [ ] Wireframes or mockups cover the main shopping journey.
- [ ] Design decisions about navigation, layout, colour, and accessibility are explained.
- [ ] The README links to the relevant documentation.
- [ ] External code, libraries, and assets are attributed where required.

### Supporting Documentation

- Business Model
- Database Schema
- ER Diagram
- Design Rationale
- Wireframes

### US-17 — Document the marketing strategy and Facebook evidence (C)

**Priority:** 🟢 Supporting

**User story:** As a business owner, I want a documented marketing strategy and brand presence so that potential customers can discover the shop.

**Acceptance criteria**

- [ ] The marketing strategy describes the target audience and brand message.
- [ ] Marketing channels and intended outcomes are explained.
- [ ] A Facebook business page or clearly identified mockup is provided if required by the project brief.
- [ ] Screenshots or mockups are available as project evidence where appropriate.
- [ ] Newsletter signup is included in the marketing strategy.
- [ ] The README links to the strategy and relevant evidence.
- [ ] Mockups are clearly distinguished from live business pages.

### Supporting Evidence

- Marketing Strategy
- Facebook Business Page or Mockup
- Brand Positioning
- Newsletter Strategy

### US-18 — Improve testing and deployment documentation (S)

**Priority:** 🟡 High

**User story:** As a developer or assessor, I want repeatable testing and deployment instructions so that the application can be reproduced and evaluated.

**Acceptance criteria**

- [ ] Automated test instructions are documented.
- [ ] Manual test cases record steps, expected results, actual results, and pass/fail status.
- [ ] Cart, checkout, payment, order history, CRUD, and authorization flows are tested.
- [ ] Deployment instructions cover environment variables, database migrations, static files, and production settings.
- [ ] `Procfile` and `requirements.txt` are consistent with the application.
- [ ] `.env.example` documents required variable names without containing real secrets.
- [ ] The README has consistent Markdown and working internal links.
- [ ] Deployment is verified using the intended production configuration.
- [ ] Relevant testing and deployment evidence is recorded.

**Planned files**

- `docs/automated-testing.md`
- `docs/manual-testing.md`
- `docs/accessibility-testing.md`
- `docs/deployment.md`
- `README.md`
- `.env.example`
- `requirements.txt`
- `Procfile`

---
### Won't Have (This Release)
The following ideas are intentionally deferred to future releases.

## Future Enhancements

### Future Commerce Features
Discount codes
Coupons
Gift cards
Product bundles
Stock notifications
Multi-currency support

### Future Customer Features
Wishlist / favourites
Customer profiles
Saved addresses
Downloadable invoices
Repeat orders

### Future Product Features
Product reviews
Product ratings
Related products
Recently viewed products
Limited edition collections

### Future Marketing Features
Automated email campaigns
Segmented newsletters
Referral programme
Customer loyalty programme
Social media integrations

### Future Technical Improvements
REST API
Dedicated mobile application
Docker deployment
CI/CD pipeline
Advanced monitoring
Extended test coverage

