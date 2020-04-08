from django.db.models import F
from django.db.models import Sum, Count
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, BaseInFilter
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Category, Product, Slide, Brand, Type, HomepageSegment
from main.serializers import CategorySerializer, ProductSerializer, SlideSerializer, \
    TypeSerializer, BrandSerializer, SegmentSerializer, BrandDetailSerializer


def initial_data(request):
    categories_queryset = Category.objects.filter(level=1)
    categories = CategorySerializer(categories_queryset, many=True).data

    slides_queryset = Slide.objects.filter(is_active=True)
    slides = SlideSerializer(slides_queryset, many=True).data

    segments_queryset = HomepageSegment.objects.filter(is_active=True).order_by("order")
    segments = SegmentSerializer(segments_queryset, many=True).data

    return JsonResponse({
        "categories": categories,
        "slides": slides,
        "segments": segments,
    })


class ProductOrdering(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            print(ordering)
            if "bestSelling" in ordering:
                return queryset.annotate(sum=Sum('orderline__amount')).order_by('-sum')
            if "mostDiscounted" in ordering:
                return queryset.annotate(dp=F('price') - F('discounted_price')).order_by('-dp')
            else:
                return queryset.order_by(*ordering)

        return queryset


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ProductFilter(FilterSet):
    parent = NumberInFilter(field_name="parent", lookup_expr='in')
    brand = NumberInFilter(field_name="brand", lookup_expr='in')
    type = NumberInFilter(field_name="types", lookup_expr='in')
    min_price = NumberFilter(field_name="discounted_price", lookup_expr='gte')
    max_price = NumberFilter(field_name="discounted_price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['parent', "brand", "type", "min_price", "max_price"]


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Product.objects.all().filter(existStatus=1)
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, ProductOrdering, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['discounted_price', 'mostDiscounted', 'bestSelling', 'created_on']

    @action(detail=False, methods=['get'])
    def filters(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        brands_pk_list = []
        related_brands = queryset.values("brand").annotate(brand_size=Count('brand')).order_by('-brand_size').values(
            "brand")
        for dictionary in related_brands:
            brands_pk_list.append(dictionary["brand"])
        brands_queryset = Brand.objects.filter(pk__in=brands_pk_list)

        types_pk_list = []
        related_types = queryset.values("types").annotate(type_size=Count('types')).order_by('-type_size').values(
            "types")
        for dictionary in related_types:
            types_pk_list.append(dictionary["types"])
        types_queryset = Type.objects.filter(pk__in=types_pk_list)

        filters = []
        if brands_queryset.count() > 1:
            filters.append(
                {"type": "brand", "title": "برند", "items": BrandSerializer(brands_queryset, many=True).data})
        if brands_queryset.count() > 1:
            filters.append(
                {"type": "type", "title": "نوع", "items": TypeSerializer(types_queryset, many=True).data})

        return Response({"filters": filters})


class BrandViewSet(GenericViewSet, ListModelMixin):
    queryset = Brand.objects.all().annotate(product_count=Count('product')).order_by("-product_count")
    permission_classes = [AllowAny]
    serializer_class = BrandDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'fa_title']
