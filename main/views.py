from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from main.models import Category, Product
from main.serializers import CategorySerializer, ProductSerializer
from main.services import get_categories, get_all_products_of_category, get_all_products


def download_categories(request):
    get_categories("food-beverage")
    return HttpResponse("ok")


def download_products(request):
    get_all_products()
    return HttpResponse("ok")


class CategoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def main(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(level=1))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     products = Product.objects.filter(category=instance)
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['parent', 'existStatus']
    ordering = ('existStatus')
