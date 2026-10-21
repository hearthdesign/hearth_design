# Hearth Shop — Project Workflow and Refactoring Plan

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

- 🔴 **Critical:** Core functionality, payment reliability, data integrity, or security.
- 🟡 **High:** Important functionality, usability, maintainability, testing, and deployment quality.
- 🟢 **Supporting:** Documentation, marketing, and assessment evidence.

Priority indicates implementation urgency, not completion status.

## 3. Project workflow

### US-01 — Audit and preserve the existing application

**Priority:** 🔴 Critical

**Project story:** As a developer, I want to understand the existing application structure and dependencies so that I can improve the project without losing data or breaking working functionality.

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

### US-02 — Browse the product catalogue

**Priority:** 🟡 High

**Project story:** As a customer, I want to browse prints and view their details so that I can decide what to purchase.

**Acceptance criteria**

- [ ] Product listings display accurate names, descriptions, prices, and images.
- [ ] Product detail pages load correctly.
- [ ] Product information comes from the database.
- [ ] Missing or unavailable images are handled gracefully.
- [ ] Product links and navigation work correctly.
- [ ] Catalogue pages are usable on desktop, tablet, and mobile.
- [ ] Relevant automated tests pass.

**Current locations:** `shop/` and `shop/templates/shop/`.

**Possible future destination:** `catalog/`.

### US-03 — Fix add-to-cart functionality

**Priority:** 🔴 Critical

**Project story:** As a customer, I want to add products to my cart and manage quantities so that I can prepare my purchase.

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

**Current locations:** Existing cart services, views, URLs, forms, and templates under `shop/`.

**Possible future destination:** `cart/`.

### US-04 — Complete checkout and create orders

**Priority:** 🔴 Critical

**Project story:** As a customer, I want checkout to create an order containing the correct items and totals so that my purchase can be processed and tracked.

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

**Current locations:** Existing checkout services and order logic under `shop/`.

**Possible future destinations:** `orders/`, `cart/`, and `payments/`.

### US-05 — Fix Stripe redirects and checkout feedback

**Priority:** 🔴 Critical

**Project story:** As a customer, I want Stripe Checkout to return me to valid success or cancellation pages so that I understand the outcome of my checkout attempt.

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

**Current locations:** Existing checkout and Stripe services, views, URLs, and settings under `shop/` and `hearth_shop/`.

**Possible future destination:** `payments/`.

### US-06 — Verify payments and update order status

**Priority:** 🔴 Critical

**Project story:** As a customer, I want my payment to be verified by the server so that my order is marked paid only after payment has been confirmed.

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

**Current locations:** Existing Stripe and webhook services, including `shop/services/stripe.py` and `shop/services/webhooks.py`, subject to verification.

**Possible future destinations:** `payments/` and `orders/`.

### US-07 — View order history securely

**Priority:** 🔴 Critical

**Project story:** As a signed-in customer, I want to see my previous orders and their statuses so that I can track my purchases.

**Acceptance criteria**

- [ ] Successfully created orders appear in the appropriate order history.
- [ ] Each order displays its reference, date, items, quantities, total, and status.
- [ ] Customers without orders see a useful empty state.
- [ ] Customers can view only their own orders.
- [ ] Direct URL access to another customer's order is denied.
- [ ] Unauthenticated access is redirected or denied appropriately.
- [ ] Automated tests cover order ownership and permissions.

**Current locations:** Existing order models, views, URLs, and templates under `shop/`.

**Possible future destination:** `orders/`.

### US-08 — Improve authentication and authorization

**Priority:** 🔴 Critical

**Project story:** As a customer, I want secure access to my account and orders so that my personal information remains private.

**Acceptance criteria**

- [ ] Registration, login, and logout work correctly.
- [ ] Signed-in users are redirected away from login or registration pages where appropriate.
- [ ] Protected actions require authentication.
- [ ] Customers cannot grant themselves staff or administrator privileges.
- [ ] Staff-only actions enforce server-side permissions.
- [ ] Direct URL requests cannot bypass authorization.
- [ ] Forms validate submitted data and protect state-changing requests against CSRF.
- [ ] Automated tests cover authenticated, unauthenticated, and unauthorized access.

**Current locations:** Existing authentication configuration, registration templates, app URLs, views, and settings.

**Possible future destination:** `accounts/`.

### US-09 — Implement frontend product CRUD

**Priority:** 🔴 Critical

**Project story:** As an authorized staff member, I want to create, view, edit, and delete products through frontend forms so that product management does not depend exclusively on Django admin.

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

**Current locations:** Existing product models, forms, views, URLs, and templates under `shop/`.

**Possible future destination:** `catalog/`.

### US-10 — Send transactional order emails

**Priority:** 🟡 High

**Project story:** As a customer, I want to receive confirmation after my payment is verified so that I have a record of my purchase.

**Acceptance criteria**

- [ ] Confirmation emails are triggered by verified payment outcomes.
- [ ] Emails include the order reference and relevant purchase details.
- [ ] Repeated webhook events do not unintentionally send duplicate confirmations.
- [ ] Email failures are logged and handled appropriately.
- [ ] HTML and plain-text email templates are available where appropriate.
- [ ] Email configuration is managed through environment variables.
- [ ] Automated tests verify the email trigger and content.

**Current locations:** Existing email functionality, if present, and order/payment services under `shop/`.

**Possible future destination:** `notifications/`.

### US-11 — Add a dedicated newsletter signup

**Priority:** 🟡 High

**Project story:** As a visitor, I want to subscribe to a newsletter separately from the contact form so that I can choose to receive marketing updates.

**Acceptance criteria**

- [ ] A dedicated newsletter form is available on the website.
- [ ] Email addresses are validated and duplicate subscriptions are handled.
- [ ] Subscription consent and relevant records are stored appropriately.
- [ ] The privacy notice explains how subscription data is used.
- [ ] An appropriate unsubscribe process is implemented.
- [ ] Marketing messages are sent in accordance with applicable consent and privacy requirements.
- [ ] Automated tests cover signup, duplicate submissions, and consent handling.

**Current locations:** Existing forms and templates under `shop/`, if applicable.

**Possible future destination:** `marketing/`.

### US-12 — Improve contact form functionality

**Priority:** 🟡 High

**Project story:** As a visitor, I want to send an enquiry through a working contact form so that I can ask questions about products or orders.

**Acceptance criteria**

- [ ] Required fields and email addresses are validated.
- [ ] Successful submissions display a clear confirmation.
- [ ] Invalid submissions display useful error messages.
- [ ] Enquiries are stored or delivered according to the documented design.
- [ ] Contact enquiries and newsletter subscriptions are handled separately.
- [ ] Appropriate spam protection and input validation are in place.
- [ ] Automated tests cover valid and invalid submissions.

**Current locations:** Existing contact forms, views, and templates under `shop/`, if applicable.

**Possible future destination:** `contact/`.

### US-13 — Improve accessibility and responsive design

**Priority:** 🟡 High

**Project story:** As a visitor, I want an accessible and responsive interface so that I can use the shop on different devices and with different access needs.

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

**Current locations:** `hearth_shop/templates/`, `shop/templates/`, `hearth_shop/static/`, and other configured source static directories.

### US-14 — Implement SEO and error handling

**Priority:** 🟡 High

**Project story:** As a visitor or search engine crawler, I want descriptive page metadata, a sitemap, and useful error pages so that the website is easier to discover and navigate.

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

**Current locations:** `hearth_shop/urls.py`, project templates, settings, and existing app URLs.

**Possible future locations:** Project-level configuration, `pages/`, or `catalog/sitemaps.py`, where appropriate.

### US-15 — Refactor into reusable Django apps safely

**Priority:** 🟡 High

**Project story:** As a developer, I want the application divided into clear, reusable Django apps so that the project is easier to maintain and extend.

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

**Current locations:** `shop/`, `hearth_shop/`, existing migrations, and services.

**Possible future destinations:** `accounts/`, `catalog/`, `cart/`, `orders/`, `payments/`, `notifications/`, `marketing/`, `contact/`, and `pages/`.

### US-16 — Document the business model, database schema, and design

**Priority:** 🟢 Supporting

**Project story:** As an assessor or developer, I want the business purpose, target audience, database relationships, and design decisions documented so that I can understand the application and its rationale.

**Acceptance criteria**

- [ ] The business model and value proposition are explained.
- [ ] The target audience and customer needs are justified.
- [ ] The implemented database schema and model relationships are documented.
- [ ] An ER diagram reflects the actual schema.
- [ ] Wireframes or mockups cover the main shopping journey.
- [ ] Design decisions about navigation, layout, colour, and accessibility are explained.
- [ ] The README links to the relevant documentation.
- [ ] External code, libraries, and assets are attributed where required.

**Planned files**

- `docs/business-model.md`
- `docs/data-schema.md`
- `docs/erd.png`
- `docs/design-rationale.md`
- `docs/wireframes/`

### US-17 — Document the marketing strategy and Facebook evidence

**Priority:** 🟢 Supporting

**Project story:** As a business owner, I want a documented marketing strategy and brand presence so that potential customers can discover the shop.

**Acceptance criteria**

- [ ] The marketing strategy describes the target audience and brand message.
- [ ] Marketing channels and intended outcomes are explained.
- [ ] A Facebook business page or clearly identified mockup is provided if required by the project brief.
- [ ] Screenshots or mockups are available as project evidence where appropriate.
- [ ] Newsletter signup is included in the marketing strategy.
- [ ] The README links to the strategy and relevant evidence.
- [ ] Mockups are clearly distinguished from live business pages.

**Planned files**

- `docs/marketing-strategy.md`
- `docs/evidence/`

### US-18 — Improve testing and deployment documentation

**Priority:** 🟡 High

**Project story:** As a developer or assessor, I want repeatable testing and deployment instructions so that the application can be reproduced and evaluated.

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

## 4. Recommended implementation phases

### Phase 1 — Audit and establish a baseline

- US-01: Audit and preserve the existing application.
- Review the current application structure, data, migrations, and dependencies.
- Identify and document known defects.
- Establish a baseline for application behaviour.

**Expected outcome:** The current architecture and major risks are understood before structural changes begin.

### Phase 2 — Repair the purchase journey

- US-03: Fix add-to-cart functionality.
- US-04: Complete checkout and order creation.
- US-05: Fix Stripe redirects and checkout feedback.
- US-06: Verify payments and update order status.
- US-07: Verify order history and ownership.
- US-10: Add transactional order emails.

**Expected outcome:** The purchase journey is verified from cart through payment confirmation and order history, including relevant failure scenarios.

### Phase 3 — Improve security and refactor incrementally

- US-08: Improve authentication and authorization.
- US-09: Implement frontend product CRUD.
- US-15: Refactor into reusable Django apps safely.

**Expected outcome:** Responsibilities are separated where appropriate, permissions are enforced, and existing data and functionality remain intact.

### Phase 4 — Complete catalogue, UX, SEO, and supporting requirements

- US-02: Browse the product catalogue.
- US-11: Add a dedicated newsletter signup.
- US-12: Improve contact form functionality.
- US-13: Improve accessibility and responsive design.
- US-14: Implement SEO and error handling.
- US-16: Document the business model, schema, and design.
- US-17: Document the marketing strategy and Facebook evidence.
- US-18: Improve testing and deployment documentation.

**Expected outcome:** The application and its supporting documentation meet the defined functional, quality, and project requirements.

## 5. Assessment evidence checklist

- [ ] Working cart and checkout.
- [ ] Verified Stripe payment handling.
- [ ] Correct order and order-item creation.
- [ ] Secure order history and ownership checks.
- [ ] Frontend CRUD with server-side permissions.
- [ ] Automated and manual testing evidence.
- [ ] Accessibility testing results.
- [ ] ER diagram and database schema.
- [ ] Business model and target-audience rationale.
- [ ] Wireframes and design rationale.
- [ ] Sitemap, `robots.txt`, meta descriptions, and custom 404 page.
- [ ] Dedicated newsletter signup.
- [ ] Facebook page screenshots or mockups, if required.
- [ ] Marketing strategy.
- [ ] Deployment procedure and verification evidence.
- [ ] README and supporting documentation.
- [ ] GitHub development history and project tracking evidence.
