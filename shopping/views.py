from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Product
from shopping.models import Order, OrderLine
from shopping.serializers import OrderSerializer, OrderLineSerializer, \
    EditOrderLineSerializer


class OrderViewSet(GenericViewSet, CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        return Order.objects.get(owner=user, status=0)

    @action(detail=False, methods=['get'])
    def cart(self, request):
        cart = self.get_cart(request.user)
        serializer = OrderSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def edit(self, request):
        cart = self.get_cart(request.user)
        serializer = EditOrderLineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id=serializer.validated_data["product_id"])
        amount = serializer.validated_data["amount"]

        if cart.lines.filter(product=product).exists():
            order_line = cart.lines.get(product=product)
            if amount > 0:
                if order_line.amount != amount:
                    order_line.amount = amount
                    order_line.price = product.price * amount
                    order_line.save()
                return Response(OrderLineSerializer(order_line).data, status=status.HTTP_200_OK)
            else:
                order_line.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            if amount > 0:
                order_line = OrderLine.objects.create(product=product, amount=amount, price=product.price * amount,
                                                      order=cart)
                return Response(OrderLineSerializer(order_line).data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
