from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
import json
from decimal import Decimal
from .models import Product

# Create your views here.
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello, World!")


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values(
            'id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')
            available = data.get('available')

            # Validate required fields
            if not all([name, price, available is not None]):
                return HttpResponseBadRequest("Missing one or more of the required fields: 'name', 'price', 'available'")

            # Create and save the product
            product = Product(name=name, price=Decimal(
                str(price)), available=available)
            product.full_clean()
            product.save()

            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            }, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format")
        except ValidationError as e:
            return HttpResponseBadRequest(f"Invalid data: {e.messages}")

    # If HTTP method is not supported
    return HttpResponseBadRequest("Unsupported HTTP method")


@csrf_exempt
def product_detail(request, product_id):
    try:
        # Retrieve the product
        product = Product.objects.get(id=product_id)

        if request.method == 'GET':
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            })
        else:
            return HttpResponseBadRequest("Unsupported HTTP method")

    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Product with ID {product_id} does not exist")
