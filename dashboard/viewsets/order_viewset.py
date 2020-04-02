from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounting.models import Seller
from dashboard.serializers import OrderListSerializer, OrderSerializer, OrderRetrieveSerializer
from main.models import Product
from shopping.models import Order


class OrderViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                   DestroyModelMixin):
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderSerializer
        if self.action == 'retrieve':
            return OrderRetrieveSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def meta_data(self, request):
        return Response({
            "columns": [
                {
                    "label": "خریدار",
                    "name": "owner"
                }, {
                    "label": "تاریخ",
                    "name": "created_on"
                }, {
                    "label": "وضعیت",
                    "name": "status"
                }, {
                    "label": "کد",
                    "name": "code"
                }, {
                    "label": "قیمت",
                    "name": "price"
                }
            ],
            "fields": [
                {
                    "label": "خریدار",
                    "type": "select",
                    "options": [{"value": seller.pk, "label": seller.user.username} for seller in
                                Seller.objects.all()],
                    "name": "owner"
                }, {
                    "label": "وضعیت",
                    "type": "text",
                    "name": "status"
                }, {
                    "label": "آیتم ها",
                    "type": "multi",
                    "fields": [
                        {
                            "label": "محصول",
                            "type": "select",
                            "options": [{"value": product.pk, "label": product.title} for product in
                                        Product.objects.filter(existStatus=1)],
                            "name": "product"
                        }, {
                            "label": "تعداد",
                            "type": "number",
                            "name": "amount"
                        },
                    ],
                    "name": "lines"
                }
            ]})
