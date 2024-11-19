from django.core.management.base import BaseCommand
from intro_app.models import Product, Customer, Order

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		Product.objects.all().delete()
		Customer.objects.all().delete()
		Order.objects.all().delete()
		
		product1 = Product.objects.create(
			name='I Fell in Love With Hope - Lancali (paperback)',
			price=39.99,
			available=True
		)
		product2 = Product.objects.create(
			name='The Invisible Life of Addie LaRue - Victoria Schwab (paperback)',
			price=39.99,
			available=True
		)
		product3 = Product.objects.create(
			name='The Seven Husbands of Evelyn Hugo - Taylor Jenkins Reid (hardcover)',
			price=45.99,
			available=True
		)
		product4 = Product.objects.create(
			name='She Gets The Girl - Rachael Lippincott (paperback)',
			price=39.99,
			available=True
        )
		product5 = Product.objects.create(
			name='Outdrawn - Deanna Grey (paperback)',
			price=39.99,
			available=True
        )
		
		customer1 = Customer.objects.create(
			name='Molly Parker',
			address='4200 Fifth Ave, Pittsburgh, PA 15260, United States'
		)
		customer2 = Customer.objects.create(
			name='Alex Blackwood',
			address='4210 Fifth Ave, Pittsburgh, PA 15260, United States'
		)
		customer3 = Customer.objects.create(
			name='Cora Myers',
			address='4220 Fifth Ave, Pittsburgh, PA 15260, United States'
		)
		
		order1 = Order.objects.create(
			customer=customer1,
			status='new'
		)
		order1.products.add(product1)
		order1.products.add(product2)
		order2 = Order.objects.create(
			customer=customer2,
			status='new'
		)
		order2.products.add(product3)
		order2.products.add(product4)
		order3 = Order.objects.create(
			customer=customer3,
			status='new'
		)
		order3.products.add(product4)
		order3.products.add(product5)
		self.stdout.write("Data created successfully.")