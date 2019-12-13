from rest_framework import status
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Product
from shopping.models import Order, OrderLine
from shopping.serializers import OrderSerializer, CreateOrderSerializer


class OrderViewSet(GenericViewSet, CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_cart(self, seller):
        if Order.objects.filter(owner=seller, status=0).count()>0:
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


    # @action(detail=False, methods=['post'])
    # def edit(self, request):
    #     cart = self.get_cart(request.user)
    #     serializer = EditOrderLineSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     product = Product.objects.get(id=serializer.validated_data["product_id"])
    #     amount = serializer.validated_data["amount"]
    #
    #     if cart.lines.filter(product=product).exists():
    #         order_line = cart.lines.get(product=product)
    #         if amount > 0:
    #             if order_line.amount != amount:
    #                 order_line.amount = amount
    #                 order_line.price = product.price * amount
    #                 order_line.save()
    #             return Response(OrderLineSerializer(order_line).data, status=status.HTTP_200_OK)
    #         else:
    #             order_line.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #
    #     else:
    #         if amount > 0:
    #             order_line = OrderLine.objects.create(product=product, amount=amount, price=product.price * amount,
    #                                                   order=cart)
    #             return Response(OrderLineSerializer(order_line).data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(status=status.HTTP_204_NO_CONTENT)
