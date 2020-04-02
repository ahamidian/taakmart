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

from accounting.models import User, Seller
from dashboard.serializers import ProductSerializer, ProductListSerializer, SellerListSerializer, SellerSerializer
from main.models import Category, Product, Slide, Brand, Type

from main.services import get_categories, get_all_products


class SellerViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Seller.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SellerListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return SellerSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def meta_data(self, request):
        return Response({
            "columns": [
                {
                    "label": "نام",
                    "name": "first_name"
                }, {
                    "label": "نام خانوادگی",
                    "name": "last_name"
                }, {
                    "label": "شماره همراه",
                    "name": "phone_number"
                },  {
                    "label": "آدرس",
                    "name": "address"
                },
            ],
            "fields": [
                {
                    "label": "first name",
                    "type": "text",
                    "name": "first_name"
                }, {
                    "label": "last name",
                    "type": "text",
                    "name": "last_name"
                }, {
                    "label": "phone number",
                    "type": "text",
                    "name": "phone_number"
                } , {
                    "label": "home phone",
                    "type": "text",
                    "name": "home_phone"
                }, {
                    "label": "address",
                    "type": "text",
                    "name": "address"
                },{
                    "label": "verification code",
                    "type": "number",
                    "name": "verification_code"
                },{
                    "label": "latitude",
                    "type": "number",
                    "name": "latitude"
                },{
                    "label": "longitude",
                    "type": "number",
                    "name": "longitude"
                }, {
                    "label": "map",
                    "type": "map",
                    "name": "map"
                }
            ]})
