from django.db import models
from user.models import User
from product.models import Product


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    access = models.BooleanField(blank=False, null=False)
