from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from main.models import Product
from main.serializers import ProductSerializer
from shopping.models import Order, OrderLine


class OrderLineSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderLine
        fields = (
            'id',
            "amount",
            "price",
            "product",
        )


class OrderSerializer(ModelSerializer):
    lines = OrderLineSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = (
            'created_on',
            'status',
            'description',
            'code',
            'lines',
        )

    # def create(self, validated_data):
    #     all_stuff_data = validated_data.pop('stuffs')
    #
    #     user = self.context["request"].user
    #     order_service = OrderService(user)
    #     order = order_service._get_order()
    #     user_stuffs = []
    #     for one_stuff in all_stuff_data:
    #         stuff = Stuff.objects.get(label_id=one_stuff.get('label_id'), weight=one_stuff.get('weight'))
    #         user_stuffs.append(stuff.pk)
    #         order_service.insert_stuff(stuff, one_stuff.get('amount'))
    #
    #     order.orderstuff_set.exclude(stuff_id__in=user_stuffs).delete()
    #     order_service.check_shipping(order)
    #     return order


class EditOrderLineSerializer(Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class CreateOrderLineSerializer(Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    price = serializers.IntegerField()


class CreateOrderSerializer(Serializer):
    lines = CreateOrderLineSerializer(many=True)
