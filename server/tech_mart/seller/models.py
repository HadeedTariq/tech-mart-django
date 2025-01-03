from django.db import models
from account.models import User


class PRODUCT_CATEGORIES(models.TextChoices):
    MOBILE = "mobile", "Mobile"
    LAPTOP = "laptop", "Laptop"
    CPU = "cpu", "CPU"
    RAM = "ram", "RAM"
    GPU = "gpu", "GPU"
    SSD = "ssd", "SSD"
    MONITOR = "monitor", "Monitor"
    MOUSE = "mouse", "Mouse"
    KEYBOARD = "keyboard", "Keyboard"


class PRODUCT_TYPES(models.TextChoices):
    NEW = "New", "New"
    USED = "Used", "Used"


class Product(models.Model):
    product_title = models.CharField(max_length=255)
    product_description = models.TextField()
    product_category = models.CharField(
        max_length=50, choices=PRODUCT_CATEGORIES.choices
    )
    product_image = models.URLField()
    product_seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=4, choices=PRODUCT_TYPES.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
