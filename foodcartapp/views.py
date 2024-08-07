from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json

from .models import Product, OrderItem, OrderDetail


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    try:
        raw_order = request.data
        print(raw_order)
        order_details = OrderDetail.objects.create(
            firstname=raw_order['firstname'],
            lastname=raw_order['lastname'],
            phonenumber=raw_order['phonenumber'],
            address=raw_order['address'],
        )
        for product in raw_order['products']:
            OrderItem.objects.create(
                products=get_object_or_404(Product, id=product['product']),
                order=get_object_or_404(OrderDetail, id=order_details.id),
                quantity=product['quantity']
            )
        return Response(raw_order)
    except ValueError as e:
        return Response({
            'error': e,
        })
