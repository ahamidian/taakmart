from rest_framework import status
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Product
from shopping.models import Order, OrderLine
from shopping.serializers import OrderSerializer, CreateOrderSerializer


class OrderViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(owner=request.user.seller)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_cart(self, seller):
        if Order.objects.filter(owner=seller, status=0).count() > 0:
            return Order.objects.get(owner=seller, status=0)
        else:
            return Order.objects.create(owner=seller)

    @action(detail=False, methods=['get'])
    def cart(self, request):
        cart = self.get_cart(request.user.seller)
        serializer = OrderSerializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cart = self.get_cart(request.user.seller)
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lines = serializer.validated_data["lines"]
        wrong_price_products = []
        for line in lines:
            product = Product.objects.get(id=line["product_id"])
            amount = line["amount"]
            price = line["price"]
            if product.discounted_price * amount == price:
                OrderLine.objects.create(order=cart, product=product, amount=amount, price=price)
            else:
                wrong_price_products.append(product)

        if wrong_price_products.__len__() == 0:
            cart.status = 1
            cart.save()
            return Response(OrderSerializer(cart).data, status=status.HTTP_201_CREATED)
        else:
            pass
