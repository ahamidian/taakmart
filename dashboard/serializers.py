from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from accounting.models import Seller, User, Company
from main.models import Category, Product, Brand, Type
from shopping.models import OrderLine, Order


class CategoryListSerializer(ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "pk",
            "title",
            "image",
            "is_leaf",
            "level",
            "parent"
        ]

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.title
        return ""


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "pk",
            "title",
            "image",
            "parent"
        ]
        extra_kwargs = {'pk': {'read_only': True}}


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'title',
            'id',
        )


class ProductListSerializer(ModelSerializer):
    brand = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "pk",
            "title",
            "price",
            "discounted_price",
            "image",
            "existStatus",
            "brand",
            "parent",
        ]

    def get_brand(self, obj):
        return obj.brand.title

    def get_parent(self, obj):
        return obj.parent.title


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "pk",
            "title",
            "price",
            "discounted_price",
            "image",
            "existStatus",
            "brand",
            "parent",
        ]
        extra_kwargs = {'pk': {'read_only': True}}


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = (
            'title',
            'id',
        )


class SellerListSerializer(ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = [
            "pk",
            "phone_number",
            "first_name",
            "last_name",
            "home_phone",
            "address",
            "latitude",
            "longitude",
            "verification_code",
        ]

    def get_phone_number(self, obj):
        return obj.user.username

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class SellerSerializer(ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True, default="")
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True, default="")

    class Meta:
        model = Seller
        fields = [
            "pk",
            "phone_number",
            "first_name",
            "last_name",
            "home_phone",
            "address",
            "latitude",
            "longitude",
            "verification_code",
        ]
        extra_kwargs = {'pk': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            is_seller=True,
            username=validated_data.pop('phone_number'),
            first_name=validated_data.pop('first_name'),
            last_name=validated_data.pop('last_name'),
        )
        user.set_password(validated_data['verification_code'])
        user.save()
        seller = Seller.objects.create(user=user, **validated_data)
        return seller

    def update(self, instance, validated_data):
        instance.user.username = validated_data.pop('phone_number')
        instance.user.first_name = validated_data.pop('first_name')
        instance.user.last_name = validated_data.pop('last_name')
        instance.user.save()
        return super(SellerSerializer, self).update(instance, validated_data)


class CompanyListSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "pk",
            "username",
            "name",
        ]

    def get_username(self, obj):
        return obj.user.username


class CompanySerializer(ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = [
            "pk",
            "username",
            "password",
            "name",
        ]
        extra_kwargs = {'pk': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            is_company=True,
            username=validated_data.pop('username'),
        )
        user.set_password(validated_data.pop('password'))
        user.save()
        company = Company.objects.create(user=user, **validated_data)
        return company

    def update(self, instance, validated_data):
        instance.user.username = validated_data.pop('username')
        instance.user.set_password(validated_data.pop('password'))
        instance.user.save()
        return super(CompanySerializer, self).update(instance, validated_data)


class OrderLineSerializer(ModelSerializer):
    class Meta:
        model = OrderLine
        fields = (
            'id',
            "amount",
            "price",
            "product",
        )


class CreateOrderLineSerializer(Serializer):
    product = serializers.IntegerField()
    amount = serializers.IntegerField()


class OrderListSerializer(ModelSerializer):
    price = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "pk",
            "owner",
            "created_on",
            "status",
            "code",
            "price",
        ]
        extra_kwargs = {'pk': {'read_only': True}}

    def get_price(self, obj):
        sum = 0
        for line in obj.lines.all():
            sum = sum + line.price
        return sum

    def get_owner(self, obj):
        return obj.owner.user.username


class OrderRetrieveSerializer(ModelSerializer):
    lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "pk",
            "owner",
            "created_on",
            "status",
            "code",
            "lines",
        ]
        extra_kwargs = {'pk': {'read_only': True}}


class OrderSerializer(ModelSerializer):
    lines = CreateOrderLineSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            "pk",
            "owner",
            "status",
            "lines",
        ]
        extra_kwargs = {'pk': {'read_only': True}}

    def create(self, validated_data):
        order = Order.objects.create(owner=validated_data.pop('owner'), status=validated_data.pop('status'))
        for line in validated_data.pop('lines'):
            product = Product.objects.get(id=line["product"])
            amount = line["amount"]
            OrderLine.objects.create(order=order, product=product, amount=amount, price=amount * product.price)

        return order

    def update(self, instance, validated_data):
        request_lines=validated_data.pop('lines')

        for order_line in instance.lines.all():
            if order_line.product.id not in [line["product"] for line in request_lines]:
                order_line.delete()

        for line in request_lines:
            product = Product.objects.get(id=line["product"])
            amount = line["amount"]
            order_line, created = OrderLine.objects.get_or_create(order=instance, product=product,
                                                                  defaults={'amount': amount,
                                                                            'price': amount * product.price})
            if not created:
                order_line.amount=amount
                order_line.price=amount*product.price
                order_line.save()

        return super(OrderSerializer, self).update(instance, validated_data)
