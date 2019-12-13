import re

from random import randint

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import Category, Product, Slide, Brand, Type


class SimpleCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "image",
        ]

    def get_children(self, obj):
        return CategorySerializer(Category.objects.filter(parent=obj), many=True).data


class CategorySerializer(ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "image",
            "children",
        ]

    def get_children(self, obj):
        return SimpleCategorySerializer(Category.objects.filter(parent=obj), many=True).data


class ProductSerializer(ModelSerializer):
    # img = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "discounted_price",
            "image",
            "existStatus",
            "brand",
            # "types",
            "parent",
        ]

    # def get_img(self, obj):
    #     if obj.img:
    #         return "http://192.168.1.8:8000" + obj.img.url
    #     return obj.pic


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'title',
            'id',
        )


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = (
            'title',
            'id',
        )


class SlideSerializer(ModelSerializer):
    class Meta:
        model = Slide
        fields = [
            "id",
            "title",
            "image",
            "internal_link",
            "external_link",
        ]
