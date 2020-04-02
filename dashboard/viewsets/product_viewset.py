from django.db.models import F
from django.db.models import Sum, Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, BaseInFilter, CharFilter
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from dashboard.serializers import ProductSerializer, ProductListSerializer
from main.models import Category, Product, Slide, Brand, Type

from main.services import get_categories, get_all_products


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ProductFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr='contains')
    parent = NumberInFilter(field_name="parent", lookup_expr='in')
    brand = NumberInFilter(field_name="brand", lookup_expr='in')
    type = NumberInFilter(field_name="types", lookup_expr='in')
    min_price = NumberFilter(field_name="discounted_price", lookup_expr='gte')
    max_price = NumberFilter(field_name="discounted_price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['title', 'parent', "brand", "type", "min_price", "max_price"]


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                     DestroyModelMixin):
    queryset = Product.objects.all().filter(existStatus=1)
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['discounted_price', 'price', "brand", "title", "parent", "existStatus"]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create' or self.action == 'update':
            return ProductSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def meta_data(self, request):
        return Response({
            "columns": [
                {
                    "label": "نام",
                    "name": "title"
                }, {
                    "label": "قیمت",
                    "name": "price"
                }, {
                    "label": "قیمت با تخفیف",
                    "name": "discounted_price"
                }, {
                    "label": "برند",
                    "name": "brand"
                }, {
                    "label": "دسته بندی",
                    "name": "parent"
                }
            ],
            "fields": [
                {
                    "label": "نام",
                    "type": "text",
                    "name": "title"
                }, {
                    "label": "قیمت",
                    "type": "number",
                    "name": "price"
                }, {
                    "label": "قیمت با تخفیف",
                    "type": "number",
                    "name": "discounted_price"
                }, {
                    "label": "وضعیت موجودی",
                    "type": "select",
                    "options": [
                        {"value": 1, "label": 'existed'},
                        {"value": 2, "label": 'coming soon'},
                        {"value": 3, "label": 'out of stock'},
                    ],
                    "name": "existStatus"
                }, {
                    "label": "برند",
                    "type": "select",
                    "options": [{"value": brand.id, "label": brand.title} for brand in
                                Brand.objects.all()],
                    "name": "brand"
                }, {
                    "label": "دسته بندی",
                    "type": "select",
                    "options": [{"value": category.id, "label": category.title} for category in
                                Category.objects.filter(is_leaf=True)],
                    "name": "parent"
                }, {
                    "label": "تصویر",
                    "type": "text",
                    "name": "image"
                }
            ],
            "filters": [
                {
                    "label": "نام",
                    "type": "text",
                    "name": "title"
                }, {
                    "label": "برند",
                    "type": "select",
                    "options": [{"value": brand.id, "label": brand.title} for brand in
                                Brand.objects.all()],
                    "name": "brand"
                }, {
                    "label": "وضعیت",
                    "type": "select",
                    "options": [
                        {"value": 1, "label": 'existed'},
                        {"value": 2, "label": 'coming soon'},
                        {"value": 3, "label": 'out of stock'},
                    ],
                    "name": "existStatus"
                }, {
                    "label": "دسته بندی",
                    "type": "select",
                    "options": [{"value": category.id, "label": category.title} for category in
                                Category.objects.filter(is_leaf=True)],
                    "name": "parent"
                },
            ],
            "bulk_edit": [
                {
                    "label": "وضعیت موجودی",
                    "type": "select",
                    "options": [
                        {"value": 1, "label": 'existed'},
                        {"value": 2, "label": 'coming soon'},
                        {"value": 3, "label": 'out of stock'},
                    ],
                    "name": "existStatus"
                }, {
                    "label": "برند",
                    "type": "select",
                    "options": [{"value": brand.id, "label": brand.title} for brand in
                                Brand.objects.all()],
                    "name": "brand"
                }, {
                    "label": "دسته بندی",
                    "type": "select",
                    "options": [{"value": category.id, "label": category.title} for category in
                                Category.objects.filter(is_leaf=True)],
                    "name": "parent"
                },
            ]
    
        })
