from django.test import TestCase
from intro_app.models import Product, Customer, Order
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product',
                                              price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product',
                                                  price=-1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                price=9.99, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='', price=9.99, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_missing_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='No price product', available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_availability(self):
        temp_product = Product.objects.create(
            name='Default availability product', price=10.00
        )
        self.assertFalse(temp_product.available)

    def test_create_product_with_name_length_edge_case(self):
        max_length_name = 'a' * 255
        temp_product = Product.objects.create(
            name=max_length_name, price=19.99, available=True
        )
        self.assertEqual(temp_product.name, max_length_name)

    def test_create_product_with_name_exceeding_length(self):
        with self.assertRaises(ValidationError):
            too_long_name = 'a' * 256
            temp_product = Product(
                name=too_long_name, price=5.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_minimum_price(self):
        temp_product = Product.objects.create(
            name='Minimum price product', price=0.01, available=True
        )
        self.assertEqual(temp_product.price, 0.01)

    def test_create_product_with_maximum_price(self):
        temp_product = Product.objects.create(
            name='Maximum price product', price=999.99, available=True
        )
        self.assertEqual(temp_product.price, 999.99)

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Invalid price format', price=9.999, available=True
            )
            temp_product.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(
            name='John Doe', address='123 Main St')
        self.assertEqual(customer.name, 'John Doe')
        self.assertEqual(customer.address, '123 Main St')

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(address='123 Main St')
            customer.full_clean()

    def test_create_customer_with_blank_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address='123 Main St')
            customer.full_clean()

    def test_create_customer_with_missing_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='John Doe')
            customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='John Doe', address='')
            customer.full_clean()

    def test_create_customer_with_edge_name_length(self):
        max_length_name = 'a' * 100
        customer = Customer.objects.create(
            name=max_length_name, address='123 Main St')
        self.assertEqual(customer.name, max_length_name)

        with self.assertRaises(ValidationError):
            too_long_name = 'a' * 101
            customer = Customer(name=too_long_name, address='123 Main St')
            customer.full_clean()


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="John Doe",
            address="123 Elm Street"
        )

        self.product1 = Product.objects.create(
            name="Widget A",
            price=50.00,
            available=True
        )
        self.product2 = Product.objects.create(
            name="Widget B",
            price=100.00,
            available=True
        )
        self.product3 = Product.objects.create(
            name="Widget C",
            price=100.00,
            available=False
        )

    def test_order_creation_with_valid_data(self):
        temp_order = Order.objects.create(
            customer=self.customer
        )
        temp_order.products.add(self.product1, self.product2)
        self.assertEqual(temp_order.customer, self.customer)
        self.assertEqual(temp_order.status, "new")
        self.assertIn(self.product1, temp_order.products.all())

    def test_order_creation_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            temp_order = Order(
                status="new"
            )
            temp_order.full_clean()  # Validate model instance

    def test_order_total_price_with_valid_products(self):
        temp_order = Order.objects.create(
            customer=self.customer
        )
        temp_order.products.add(self.product1, self.product2)
        total_price = temp_order.order_price()
        self.assertEqual(total_price, self.product1.price +
                         self.product2.price)

    def test_order_total_price_with_no_products(self):
        temp_order = Order.objects.create(
            customer=self.customer
        )
        self.assertEqual(temp_order.order_price(), 0)

    def test_order_fulfillable_with_all_products_available(self):
        temp_order = Order.objects.create(
            customer=self.customer
        )
        temp_order.products.add(self.product1, self.product2)
        self.assertTrue(temp_order.fullfillable())

    def test_order_fulfillable_with_unavailable_products(self):
        temp_order = Order.objects.create(
            customer=self.customer
        )
        temp_order.products.add(self.product3)
        self.assertFalse(temp_order.fullfillable())  # Order with self.product2, which is unavailable
