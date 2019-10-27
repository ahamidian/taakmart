import re

from random import randint

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import Category, Product


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
            # "brand",
            # "types",
            "parent",
        ]

    # def get_img(self, obj):
    #     if obj.img:
    #         return "http://192.168.1.8:8000" + obj.img.url
    #     return obj.pic

#
# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = MarketUser
#         fields = ("username", "first_name", "last_name", "email", "addresses", "password")
#         extra_kwargs = {'password': {'write_only': True}}
#
#
# class UserGetCodeSerializer(serializers.Serializer):
#     username = serializers.CharField()
#
#     def validate_username(self, data):
#         if re.match('^09\d{9}$', data):
#             return data
#         raise ValidationError("wrong phone number")
#
#     def create(self, validated_data):
#         market_user = MarketUser.objects.get(phone_number=validated_data["username"])
#         delta_time = timezone.now() - market_user.verification_code_created_on
#         if market_user.verification_code is None or delta_time.days > 0:
#             verification_code = str(randint(10000, 99999))
#             market_user.verification_code = verification_code
#             market_user.verification_code_created_on = timezone.now()
#             market_user.save()
#             market_user.user.set_password(verification_code)
#         # SmsServices.send_verification_code(user)
#         return market_user
#
#
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super(MyTokenObtainPairSerializer, self).validate(attrs)
#         serializer = UserSerializer(instance=self.user)
#         data['user'] = serializer.data
#         return data
