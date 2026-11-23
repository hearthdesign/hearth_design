from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from shop.storage_cloudinary import CloudinaryMediaStorage


def _generate_unique_slug(instance, source_value, max_length=200):
    base_slug = slugify(source_value)[:max_length] or "item"
    slug = base_slug
    model_cls = instance.__class__
    counter = 2
    while model_cls.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        suffix = f"-{counter}"
        slug = f"{base_slug[: max_length - len(suffix)]}{suffix}"
        counter += 1
    return slug


# Parent Category Model
class Category(models.Model):
    TYPE_CHOICES = [
        ("info", _("Info")),
        ("print", _("Print")),
        ("blog", _("Blog")),
        ("general", _("General")),
    ]
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    description = models.TextField(blank=True)

    # Define the context in which the category is used
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="general")
    # Allows hierarchical nesting of categories
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
    )
    # Optional visual representation for category
    image = models.ImageField(
        upload_to="category_images/",
        storage=CloudinaryMediaStorage(),
        blank=True,
        null=True,
    )
    # Hide category without deleting if not in use
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["type"]),
            models.Index(fields=["title"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(self, self.title, max_length=200)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Theme Model
class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=120)
    icon = models.ImageField(
        upload_to="theme_icons/",
        storage=CloudinaryMediaStorage(),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(self, self.name, max_length=120)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Base Print model
class Print(models.Model):
    TYPE_CHOICES = [
        ("photo", _("Photography")),
        ("illustration", _("Illustration")),
    ]
    FORMAT_CHOICES = [
        ("metal", _("Metal Print")),
        ("wood", _("Wood Print")),
        ("paper", _("Paper Print")),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES, blank=True)
    size = models.CharField(max_length=50, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    # Cloudinary for images
    image = models.ImageField(
        upload_to="prints/%Y/%m/%d",
        storage=CloudinaryMediaStorage(),
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal("50.00")
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    themes = models.ManyToManyField("Theme", blank=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["title"]
        verbose_name = _("Print")
        verbose_name_plural = _("Prints")
        indexes = [
            models.Index(fields=["price"]),
        ]

    @property
    def avg_rating(self):
        result = self.reviews.aggregate(avg=Avg("rating"))
        return round(result["avg"], 1) if result["avg"] else 0.0

    @property
    def num_reviews(self):
        return self.reviews.count()

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def thumbnail_url(self):
        if self.image:
            return self.image.url.replace(
                "/upload/", "/upload/f_auto,q_auto,c_fill,w_300,h_300/"
            )
        return ""

    @property
    def modal_url(self):
        if self.image:
            return self.image.url.replace("/upload/", "/upload/f_auto,q_auto,w_1200/")
        return ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(self, self.title, max_length=200)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Contact submission model
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_hash = models.CharField(max_length=64, default="unknown")  # SHA-256 hash of IP
    user_agent = models.TextField(default="unknown")
    submitted_at = models.DateTimeField(default=timezone.now)
    marketing_consent = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Contact Submission")
        verbose_name_plural = _("Contact Submissions")

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"


class Review(models.Model):
    print_item = models.ForeignKey(
        Print, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # 1 to 5 stars
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        reviewer = self.user.username if self.user else _("Anonymous")
        return f"{self.rating} Stars by {reviewer} for {self.print_item.title}"
