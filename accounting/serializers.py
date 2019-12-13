import re

from random import randint

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounting.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}


class UserGetCodeSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, data):
        if re.match('^09\d{9}$', data):
            return data
        raise ValidationError("wrong phone number")

    def create(self, validated_data):
        user = User.objects.get(username=validated_data["username"])
        seller = user.seller
        delta_time = timezone.now() - seller.verification_code_created_on
        if seller.verification_code is None or delta_time.days > 0:
            verification_code = str(randint(10000, 99999))
            verification_code = "11111"
            seller.verification_code = verification_code
            seller.verification_code_created_on = timezone.now()
            user.set_password(verification_code)
            seller.save()
            user.save()
        # SmsServices.send_verification_code(user)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        serializer = UserSerializer(instance=self.user)
        data['user'] = serializer.data
        return data
