from email.policy import default
from django.db import models
from django.conf import settings
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    price_m = models.FloatField(default=0)
    price_a = models.FloatField(default=0)
    unique_feature = models.JSONField(default={}) 
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(null=True,blank=True, default='/placeholder.png')
    # imageII = models.ImageField(null=True,blank=True, default='/placeholder.png')
    # imageIII = models.ImageField(null=True,blank=True, default='/placeholder.png')
    description = models.TextField(null=True, blank=True)
    cat = models.CharField(max_length=200, null=True, blank=True)
    d_cat = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7,decimal_places=2, null=True, blank=True)
    discount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} for Rs.{self.price_m} or AC.{self.price_a}"

    def __len__(self):
        return len(self.unique_feature)


class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


# class Cart(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     product
    