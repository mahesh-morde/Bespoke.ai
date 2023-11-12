from django.db import models

class UserCredentials(models.Model):
    customer_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True, null=True)
    preferred_category = models.CharField(max_length=255, blank=True, null=True)
    

class Meta:
        app_label = 'user_management'

class Catalog(models.Model):
    product_id = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    rank = models.IntegerField()
    brand_name = models.CharField(max_length=255)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_link = models.URLField()

    def __str__(self):
        return self.product_description


