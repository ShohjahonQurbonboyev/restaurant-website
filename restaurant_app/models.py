from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20)
    total = models.IntegerField(default=0)  # ✅
    created_at = models.DateTimeField(auto_now_add=True)


   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("MenuItem", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.item.price * self.qty



class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("cake", "Cake"),
        ("muffins", "Muffins"),
        ("croissant", "Croissant"),
        ("bread", "Bread"),
        ("tart", "Tart"),
        ("favorite", "Favorite"),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="favorite")
    short_desc = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to="recipes/", blank=True, null=True)

    prep_time = models.PositiveIntegerField(default=10)   # minut
    cook_time = models.PositiveIntegerField(default=15)   # minut
    servings = models.PositiveIntegerField(default=2)

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Feedback(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at:%d.%m %H:%M}"
