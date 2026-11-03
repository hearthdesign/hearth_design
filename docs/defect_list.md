# Known Defects List

## Upload Page (`upload.html`)

### Navigation / UX Improvements

Add a clearly visible button to allow users to leave the upload process without relying on:

- The navigation bar
- The browser back button

Possible button labels:

- **Cancel**
- **Back**
- **Back to Home**
- **Back to Gallery**
- **Continue Shopping** (if appropriate for the user journey)

**Action Required:**

- Determine the most suitable label and placement.
- Review other pages for consistency and consider implementing a similar navigation pattern site-wide.

---

## Language Switcher

### Missing Functionality

- Language switcher is not available on the upload page.
- Verify whether it is missing from any other templates.

---

## Admin Area

### Change Password Form

**Issue:**

- Accessing the password change form currently results in a **500 Server Error**.

**Action Required:**

- Investigate error logs.
- Verify URL configuration, templates, and authentication views.
- Test password change functionality in both development and production environments.

---

## Site-Wide Issues

### Checkout Status Messages

#### Failed Checkout with Empty Cart

**Issue:**

- No clear status or feedback message is displayed when a checkout attempt fails because the shopping cart is empty.

**Expected Behavior:**

- Display a user-friendly message such as:

> "Your cart is empty. Please add items before proceeding to checkout."

---

### Order Confirmation Flow

#### "View Order" Returns No Order

**Issue:**

- An order confirmation appears to be displayed, but selecting **View Order** results in:

> "No order has been created."

**Possible Causes:**

- Order object not being saved.
- Session data lost before order creation.
- Redirect occurring before transaction completion.
- Incorrect order lookup logic.

**Action Required:**

- Verify order creation workflow.
- Confirm database records are created successfully.
- Validate session and redirect handling after checkout.
- Test successful and failed checkout scenarios.

### Missing PWA Icons

**Status:** Open

**Files missing:**

- `android-chrome-192x192.png`
- `android-chrome-512x512.png`

**Impact:**

Browser console and Heroku logs contain repeated 404 errors.

---

## Checkout & Stripe Integration

### Orders Not Created After Successful Payment

**Status:** Open

**Priority:** High

**Issue:**

Users are redirected to the Stripe success page after payment, but no order is created in the database.

**Evidence:**

- Stripe checkout session is created successfully.
- Payment completes successfully in Stripe Test Mode.
- User is redirected to the success page.
- Order history displays:

> "You have no past orders."

- Database query returns:

```python
Order.objects.count()
0
```

**Investigation Findings:**

- `client_reference_id` is being passed correctly to Stripe.
- Stripe webhook endpoint receives requests.
- No orders exist in the database after successful payment.

**Potential Cause:**

Webhook processing may not complete successfully after checkout.

---

### Stripe Webhook Returns Redirect (302)

**Status:** Open

**Priority:** High

**Issue:**

Heroku logs show:

```text
POST /shop/stripe/webhook/ HTTP/1.1 302
```

A Stripe webhook endpoint should normally return:

```text
200 OK
```

instead of a redirect response.

**Impact:**

- Webhook event processing may not execute.
- Orders may not be created.
- Cart items may not be cleared after payment.

**Investigation Notes:**

Project currently routes:

```python
path("shop/", include("shop.urls"))
```

through:

```python
i18n_patterns(...)
```

which may interfere with Stripe's server-to-server requests.

**Planned Fix:**

Move the Stripe webhook route outside `i18n_patterns` to provide a language-independent endpoint.

---

### Missing Webhook Processing Verification

**Status:** Open

**Priority:** High

**Issue:**

Insufficient logging makes it difficult to determine where webhook processing stops.

**Action Taken:**

Additional diagnostics added:

```python
print("WEBHOOK RECEIVED")
print("EVENT TYPE:", event["type"])
print("USER ID:", user_id)
print("Creating order...")
print("ORDER CREATED:", order.id)
```

**Next Step:**

Review Heroku logs after another successful test payment.

---

## Cart

### Cart Not Cleared After Successful Payment

**Status:** Open

**Priority:** High

**Issue:**

Items remain in the cart after a successful Stripe payment.

**Expected Behaviour:**

After order creation:

```python
cart.cartitem_set.all().delete()
```

should empty the cart.

**Actual Behaviour:**

Cart contents remain unchanged.

**Possible Cause:**

Webhook processing does not reach the cart-clearing stage.

---

### Quantity Increase Function Not Updating Cart

**Status:** Open

**Priority:** Medium

**Issue:**

The quantity increase action does not always appear to update the cart.

**Current Logic:**

```python
if cart_item.quantity < cart_item.print.stock:
    cart_item.quantity += 1
    cart_item.save()
```

**Investigation Required:**

- Verify stock values.
- Verify quantity updates are persisted.
- Confirm updated values are rendered correctly in the cart template.

---

## Database

### Intermittent PostgreSQL Connection Closures

**Status:** Open

**Priority:** Medium

**Issue:**

Database connection occasionally becomes unavailable during shell operations.

**Observed Errors:**

```text
psycopg.OperationalError: the connection is closed
```

```text
SSL SYSCALL error: Software caused connection abort
```

**Notes:**

Connections can be restored manually:

```python
from django.db import connection

connection.connect()
print(connection.is_usable())
```

returns:

```python
True
```

**Investigation Required:**

- Review Neon database connection settings.
- Verify SSL configuration.
- Monitor connection stability on Heroku.

---