from django.db import models
from django.utils.text import slugify

# Parent Category Model
class Category(models.Model):
    TYPE_CHOICES = [
        ('info', 'Info'),
        ('product', 'Product'),
        ('blog', 'Blog'),
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
    

# Print product Model
class Print(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photography'),
        ('illustration', 'Illustration'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='prints/%Y/%m%d', blank=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    in_stock = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = "Print"
        verbose_name_plural = "Prints"

# Product Model
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    FORMAT_CHOICES = [
        ('poster', 'Poster'),
        ('canvas', 'Canvas'),
        ('framed', 'Framed Print'),
        ('digital', 'Digital Download'),
        ('photo-paper', 'Photo Paper'),
        ('fine-art', 'Fine Art Print'),
        ('metal', 'Metal Print'),
        ('wood', 'Wood Print'),
    ]
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    size = models.CharField(max_length=50, blank=True)
    print = models.ForeignKey(Print, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-stock']
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.print.title} - {self.sku}"
    

class Photography(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='photographies/', blank=True)
    print = models.ForeignKey(Print, on_delete=models.CASCADE, related_name='photographies')

    def __str__(self):
        return self.title

# Order Model   
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

