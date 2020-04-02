from django.db.models import F
from django.db.models import Sum, Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, BaseInFilter
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounting.models import User, Seller, Company
from dashboard.serializers import ProductSerializer, ProductListSerializer, SellerListSerializer, SellerSerializer, \
    CompanyListSerializer, CompanySerializer
from main.models import Category, Product, Slide, Brand, Type

from main.services import get_categories, get_all_products


class CompanyViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                     DestroyModelMixin):
    queryset = Company.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CompanyListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CompanySerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def meta_data(self, request):
        return Response({
            "columns": [
                {
                    "label": "نام کاربری",
                    "name": "username"
                }, {
                    "label": "نام",
                    "name": "name"
                },
            ],
            "fields": [
                {
                    "label": "نام کاربری",
                    "type": "text",
                    "name": "username"
                }, {
                    "label": "نام",
                    "type": "text",
                    "name": "name"
                }, {
                    "label": "رمز عبور",
                    "type": "password",
                    "name": "password"
                }
            ]})
