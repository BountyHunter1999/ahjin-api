from email.policy import default
from secrets import choice
from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

from django.core.validators import MinValueValidator

CAT = (
    ('E', 'Electronics'),
    ('C', 'Clothes'),
    ('O', 'Others')
)

DCAT = (
    ("Lap","Laptop"),
    ("Cam", "Camera"),
    ("M","Men Clothes"),
    ("F","Female Clothes"),
    ("B","Baby Clothes"),
    ("W","Washing Machine"),
)

DEFAULT_IMG = "http://res.cloudinary.com/sankalpa-sys/image/upload/v1657722684/jw5rqwjldedhnpxjlztc.jpg"

class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    price_m = models.FloatField(default=0, validators=[MinValueValidator(0.0)], help_text='in NPR',)
    price_a = models.FloatField(default=0, validators=[MinValueValidator(0.0)], help_text='in Ahjin Coin',)
    unique_feature = models.JSONField(default=dict) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    numReviews = models.IntegerField(null=True, blank=True, default=0)
    
    # color = models.
    featured = models.BooleanField(default=False)
    image = models.URLField(max_length=200, default=DEFAULT_IMG)
    image2 = models.URLField(max_length=200, default=DEFAULT_IMG)
    image3 = models.URLField(max_length=200, default=DEFAULT_IMG)
    # image = models.ImageField(null=True,blank=True, default='/placeholder.png')
    # imageII = models.ImageField(null=True,blank=True, default='/placeholder.png')
    # imageIII = models.ImageField(null=True,blank=True, default='/placeholder.png')
    description = models.TextField(null=True, blank=True)
    cat = models.CharField(max_length=20, choices=CAT)
    d_cat = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7,decimal_places=2, null=True, blank=True)
    discount = models.FloatField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} for Rs.{self.price_m} or AC.{self.price_a}"

    def __len__(self):
        count = 0
        try:
            print(f" unique feature is: {self.unique_feature}")
            # feature = self.unique_feature[0]
            feature = self.unique_feature
            if len(feature) > 0:
                print(f"feature {feature}")
                # for i in feature.values():
                for i in feature:
                    print(f"i is {i}")
                    count += i['count']
                return count
        except:
            return 0
    
    def clean(self):
        pass

    
    def save(self, *args, **kwargs):
        """
        Override the default save to run full_clean method
        """
        self.full_clean()
        return super(Product, self).save(*args, **kwargs)

    def count(self):
        return len(self)



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # user = models.ForeignKey(User, related_name='reviews', on_delete=models.SET_NULL, null=True)
    # name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) 

    def user_name(self):
        return self.user

    def product_name(self):
        return self.product.name

    def product_rating(self):
        return self.rating
    



# class Cart(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     product
    