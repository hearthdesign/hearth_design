# Hearth Shop — Project Workflow and Refactoring Plan


## Table of Contents

- [Hearth Shop — Project Workflow and Refactoring Plan](#hearth-shop--project-workflow-and-refactoring-plan)
  - [Table of Contents](#table-of-contents)
  - [1. Project context](#1-project-context)
  - [2. Priority legend](#2-priority-legend)
    - [MoSCoW Prioritisation](#moscow-prioritisation)
    - [Priority Colours](#priority-colours)
  - [3. Implementation phases](#3-implementation-phases)
    - [Phase 1 — Audit and establish a baseline](#phase-1--audit-and-establish-a-baseline)
    - [Phase 2 — Repair the purchase journey](#phase-2--repair-the-purchase-journey)
    - [Phase 3 — Improve security and refactor incrementally](#phase-3--improve-security-and-refactor-incrementally)
    - [Phase 4 — Complete catalogue, UX, SEO, and supporting requirements](#phase-4--complete-catalogue-ux-seo-and-supporting-requirements)
  - [4. GitHub Project Workflow](#4-github-project-workflow)
    - [Board Columns](#board-columns)
    - [Workflow](#workflow)
    - [Github Labels](#github-labels)
  - [5. Definition of Done](#5-definition-of-done)
  - [6. Assessment evidence checklist](#6-assessment-evidence-checklist)


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

### MoSCoW Prioritisation

1. Must Have (M)

These stories are essential for a functional, secure e-commerce application. Without them, the core shopping journey is incomplete.

2. Should Have (S)

These stories significantly improve the application, but are not strictly required for the first working release.

3. Could Have (C)

These features add business value but are not required for a successful first release.

4. Won't Have (This Release)

The following ideas are intentionally deferred to future releases.

### Priority Colours

- 🔴 **Critical:** Core functionality, payment reliability, data integrity, or security.
- 🟡 **High:** Important functionality, usability, maintainability, testing, and deployment quality.
- 🟢 **Supporting:** Documentation, marketing, and assessment evidence.

**Priority indicates implementation urgency, not completion status.**


## 3. Implementation phases

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


## 4. GitHub Project Workflow

The project is tracked using GitHub Issues and GitHub Projects.

### Board Columns

Backlog
Ready
In Progress
Testing / Review
Done

### Workflow

            Issue Created
                  ↓
               Backlog
                  ↓
                Ready
                  ↓
             In Progress
                  ↓
            Testing / Review
                  ↓
                 Done

### Github Labels

priority:critical
priority:high
priority:supporting

type:user-story
type:bug
type:documentation

area:backend
area:frontend
area:payments
area:security
area:testing
area:marketing
area:refactoring


## 5. Definition of Done

A user story can be moved to Done only when:

- All acceptance criteria have been satisfied.
- Relevant automated tests pass.
- Manual testing has been completed.
- Documentation has been updated.
- Existing functionality has been checked for regressions.
- The GitHub Issue reflects the completed work.


## 6. Assessment evidence checklist

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



