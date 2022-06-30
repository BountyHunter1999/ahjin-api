from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.core.validators import MinValueValidator

from products.models import Product
from django.conf import settings


PAYMENT_METHODS = (
    ('K', 'Khalti'),
    ('P', 'Paypal'),
    ('A', 'Ahjin_coin'),
)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    productChosen = models.IntegerField(null=True, blank=True, default=0)
    quantity = models.IntegerField(null=True, validators=[MinValueValidator(0)], blank=True, default=0)

    paymentMethod = models.CharField(max_length=12, choices=PAYMENT_METHODS)

    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} bought {self.product.name} with {self.get_paymentMethod_display()}"

    def product_delivered(self):
        return self.delivered

    def user_name(self):
        return self.user

    def product_name(self):
        return self.product.name

    def paid_with(self):
        return self.get_paymentMethod_display()
