from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def positive(value):
    if value <= 0:
        raise ValidationError('Value must be positive')
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[positive])
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField(auto_now_add=True)

    ORDER_STATUS_CHOICES = [
        ('new', 'New'),
        ('in_process', 'In Process'),
        ('sent', 'Sent'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new')

    def __str__(self):
        return "order id:" + str(self.id) + " status:" + self.status
    
    def order_price(self):
        return sum(p.price for p in self.products.all())
    
    def fullfillable(self):
        return all(p.available for p in self.products.all())
