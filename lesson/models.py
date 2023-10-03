from django.db import models


class Lesson(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    link = models.CharField(max_length=255,blank=False, null=False)
    duration = models.IntegerField(blank=False, null=False)
    product = models.ManyToManyField("product.Product", related_name="product")

    def __str__(self):
        return self.name

