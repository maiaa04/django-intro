from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    