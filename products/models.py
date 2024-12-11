from django.db import models

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product_images/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
