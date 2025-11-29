from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings

# Parent Category Model
class Category(models.Model):
    TYPE_CHOICES = [
        ('info', 'Info'),
        ('print', 'Print'),
        ('blog', 'Blog'),
        ('general', _('General'))
    ]
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    description = models.TextField(blank=True)
    
    # Define the context in which the category is used
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    # Allows hierarchical nesting of categories
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')
    # (Optional) visual representation for category
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    # Hide category without delete if is not in use
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['type']),
            models.Index(fields=['title']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# Theme Model
class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='theme_icons/', blank=True, null=True)

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Base Print model
class Print(models.Model):
    TYPE_CHOICES = [
        ('photo', _('Photography')),
        ('illustration', _('Illustration')),
    ]
    FORMAT_CHOICES = [
        ('metal', _('Metal Print')),
        ('wood', _('Wood Print')),
        ('paper', _('Paper Print')),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES, blank=True)
    size = models.CharField(max_length=50, blank=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='prints/%Y/%m%d', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=50.00)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)  # allow nulls for auto generation
    is_active = models.BooleanField(default=True)
    themes = models.ManyToManyField("Theme", blank=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Print"
        verbose_name_plural = "Prints"
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['price']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-generate SKU if missing
        if not self.sku:
            # Save first to get an ID if it's a new object
            super().save(*args, **kwargs)
            self.sku = f"{self.type[:3].upper()}-{self.id}"
            kwargs['force_insert'] = False  # ensure update not insert
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.sku}"
    
# Photography Model
class Photography(models.Model):
    print = models.ForeignKey(Print, on_delete=models.CASCADE, related_name='photographies')
    title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='photographies/', blank=True)
    in_stock = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    themes = models.ManyToManyField("Theme", blank=True)
    
    class Meta:
        verbose_name = _("Photography")
        verbose_name_plural = _("Photographies")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Illustration Model
class Illustration(models.Model):
    print = models.ForeignKey(Print, on_delete=models.CASCADE, related_name='illustrations')
    title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='illustrations/', blank=True)
    in_stock = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    themes = models.ManyToManyField("Theme", blank=True)

    class Meta:
        verbose_name = _("Illustration")
        verbose_name_plural = _("Illustrations")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        
# Cart model
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prints = models.ManyToManyField(Print, through='CartItem')

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    print = models.ForeignKey(Print, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return f"{self.quantity} x {self.print.title} in {self.cart.user.username}'s cart"
    

# Order model
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    prints = models.ManyToManyField(Print, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    print = models.ForeignKey(Print, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.quantity} x {self.print.title} in Order #{self.order.id}"

# Contact submission Model
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_hash = models.CharField(max_length=64, default="unknown")  # SHA-256 hash of IP
    user_agent = models.TextField(default="unknown")
    submitted_at = models.DateTimeField(default=timezone.now)
    marketing_consent = models.BooleanField(default=False)  # Marketing consent field


    class Meta:
        verbose_name = _("Contact Submission")
        verbose_name_plural = _("Contact Submissions")    

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"