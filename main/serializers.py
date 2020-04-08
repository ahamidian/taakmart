from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from main.models import Category, Product, Slide, Brand, Type, HomepageSegment


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


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'title',
            'fa_title',
            'id',
        ]

class BrandDetailSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'title',
            "image",
            "description",
            'fa_title',
            'id',
        ]


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = [
            'title',
            'id',
        ]


class ProductSerializer(ModelSerializer):
    # img = serializers.SerializerMethodField()
    brand = BrandSerializer(many=False)

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


class SegmentSerializer(ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = HomepageSegment
        fields = [
            "title",
            "query",
            "products",
            "image",
            "external_link",
        ]
