from django.db import models

# Parent Category.
class Category(models.Model):
    TYPE_CHOICES = [
        ('general', 'General'),
        ('print', 'Print'),
        ('blog', 'Blog'),
    ]
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
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

    def __str__(self):
        return self.name