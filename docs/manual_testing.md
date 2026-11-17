# Hearth Shop — Manual Testing

Areas tested:

- Navigation
- Internationalisation
- Theme filtering
- Authentication
- Cart functionality
- Checkout flow
- Contact form validation
- Responsive layouts

**Manual testing completed.**

Results:

All critical user journeys completed successfully.
Theme filtering verified across all supported languages.
Language switching verified without data loss.
Automated tests: 13 passed.
Manual tests: completed successfully.

## US-01 Audit Existing Application

### Test Case 1

Objective
Verify application runs locally.

Steps

1. Activate virtual environment.
2. Run server.

Expected Result
Homepage loads correctly.

Actual Result
Homepage loaded successfully.

Status
Pass

## US-02 Browse Product Catalogue

### Test Case 1

Objective
Verify products display correctly.

Steps
1. Open homepage.
2. Open gallery page.

Expected Result
Products display names, images and prices.

Actual Result
Products displayed correctly.

Status
Pass

---

PHOTOGRAPHY GALLERY
![alt text](image-2.png)

ILLUSTRATION GALLERY
![alt text](image-1.png)

LANGUAGES
ENGLISH
![alt text](image-3.png)
ITALIAN
![alt text](image-4.png)
GERMAN
![alt text](image-5.png)
FRENCH
![alt text](image-6.png)
PORTUGUESE
![alt text](image-7.png)
JAPANESE
![alt text](image-8.png)
CHINESE
![alt text](image-9.png)

Internationalisation applies to:

- Navigation
- Buttons
- Forms
- Validation messages
- Page titles
- Ecommerce workflow
- Cart
Stripe Checkout Verification


### Test Case 1

Objective

Verify that a successful Stripe checkout creates an order.

Steps

Add a print to the cart.
Proceed to checkout.
Complete payment using a Stripe test card.
Allow Stripe webhook processing.

Expected Result

Order created successfully.
Order appears in Order History.
Payment marked as paid.

Actual Result

Order was created successfully and displayed in Order History.

Status

Pass

---

### Test Case 2

Objective

Verify that completed orders clear the shopping cart.

Steps

Add products to cart.
Complete checkout.
Return to cart.

Expected Result

Cart is empty after payment.

Actual Result

Cart was cleared successfully.

Status

Pass

--- 

### Test Case 3

Objective

Verify duplicate Stripe webhook events do not create duplicate orders.

Steps

Trigger webhook processing.
Re-submit the same Stripe session.

Expected Result

Only one order exists for the Stripe session.

Actual Result

Duplicate order creation prevented successfully.

Status

Pass

---

- Contact form

Artwork titles and theme names remain editor-defined content and are not translated.

CHECK OUT
![alt text](image-23.png)
![alt text](image-24.png)

CART
![alt text](image-22.png)

PAYMENT
![alt text](image-10.png)

PAYAMENT CONFIRMATION
![alt text](image-11.png)
![alt text](image-25.png)

ORDER (OLD)
![alt text](image-12.png)

ORDER (NEW)
![alt text](image-13.png)
![alt text](image-26.png)

REGISTRATION
![alt text](image-21.png)

LOGIN
![alt text](image-14.png)
![alt text](image-15.png)

UPLOAD IMAGES
![alt text](image-16.png)
![alt text](image-17.png)

DJANGO ADMIN
![alt text](image-18.png)
![alt text](image-19.png)
![alt text](image-20.png)
---

## System Validation

### Django System Check

**Objective**

Verify that the Django project configuration contains no configuration, application, template, middleware, URL routing, or model issues.

**Command**

```bash
python manage.py check
```

Expected Result
System check identified no issues (0 silenced).

Actual Result
System check identified no issues (0 silenced).