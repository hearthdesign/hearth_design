# Dependency Inventory

## Framework and Application Configuration

### Django 5.2.6

Primary web framework used to implement:

- URL routing
- Views
- Templates
- Forms
- Authentication
- ORM and database access
- Internationalisation

### django-extensions 4.1

Developer tooling used for project inspection and maintenance tasks.

### dj-database-url 3.0.1

Parses database connection strings from environment variables and deployment platforms.

---

## Database

### psycopg 3.2.10

PostgreSQL database adapter used by Django in local and production environments.

---

## Payment Processing

### stripe 12.5.1

Provides:

- Stripe Checkout Sessions
- Payment processing
- Payment verification
- Webhook event handling

Used by:

- shop/services/stripe.py
- shop/services/webhooks.py

---

## Media Storage

### cloudinary 1.44.1

Cloud-based storage and delivery of product images.

### django-cloudinary-storage 0.3.0

Integrates Cloudinary with Django's file-storage system.

### django-storages 1.14.6

Provides configurable storage backends used by media and asset storage integrations.

---

## Static Files and Deployment

### whitenoise 6.11.0

Serves static assets in production environments.

### gunicorn 23.0.0

Production WSGI server used for deployment.

---

## Image Processing

### Pillow 11.3.0

Provides image processing functionality required by Django image fields.

---

## Environment Configuration

### python-decouple 3.8

Loads settings and secrets from environment variables.

### python-dotenv 1.1.1

Loads local environment variables during development.

---

## AWS / S3 Related Libraries

### boto3 1.42.65

AWS SDK.

### botocore 1.42.65

Low-level AWS functionality used by boto3.

### s3transfer 0.16.0

AWS file transfer support.

Status:

Present in requirements.txt.
Current usage should be verified during the architecture audit.

---

## Networking and HTTP Libraries

### requests 2.32.5

HTTP client library used by other packages.

### urllib3 2.5.0

HTTP transport layer.

### certifi 2025.8.3

Certificate bundle used for secure HTTPS communication.

### charset-normalizer 3.4.3

Character encoding detection.

### idna 3.10

Internationalised domain name handling.

---

## Utility Libraries

### python-dateutil 2.9.0.post0

Date parsing and manipulation.

### packaging 25.0

Version and package utilities.

### six 1.17.0

Python compatibility helpers.

### sqlparse 0.5.3

SQL formatting used internally by Django.

### typing_extensions 4.15.0

Additional typing features for Python.

### tzdata 2025.2

Time zone database.

### asgiref 3.9.1

ASGI support library required by Django.

### jmespath 1.1.0

Query language dependency used by AWS libraries.


