from rest_framework.serializers import ModelSerializer

from .models import OrderItem, OrderDetail, Product


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(
        many=True,
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = OrderDetail
        fields = '__all__'

    def create(self, validated_data):
        order_details = OrderDetail.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address'],
        )
        for product in validated_data['products']:
            product['price'] = product['product'].price

        products = [
            OrderItem(order=order_details, **fields) for fields in validated_data['products']
        ]
        return OrderItem.objects.bulk_create(products)
