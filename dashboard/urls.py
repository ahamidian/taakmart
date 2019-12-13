"""digikala_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from accounting.views import MyTokenObtainPairView, UserViewSet
from main.views import download_categories, download_products, CategoryViewSet, ProductViewSet, SlideViewSet, dashboard
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from shopping.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, base_name='categories')
router.register(r'products', ProductViewSet, base_name='products')
router.register(r'send_code', UserViewSet, base_name='send_code')
router.register(r'order', OrderViewSet, base_name='order')
router.register(r'slides', SlideViewSet, base_name='slide')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name="dashboard"),
    path('download_categories/', download_categories),
    path('download_products/', download_products),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
