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
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.apps import apps

from accounting.views import MyTokenObtainPairView, UserViewSet
from dashboard.viewsets import product_viewset, category_viewset, seller_viewset, company_viewset, order_viewset
from main.views import ProductViewSet, initial_data, BrandViewSet
from shopping.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, base_name='products')
router.register(r'brands', BrandViewSet, base_name='brands')
router.register(r'send_code', UserViewSet, base_name='send_code')
router.register(r'order', OrderViewSet, base_name='order')


dashboard_router = routers.DefaultRouter()
dashboard_router.register(r'products', product_viewset.ProductViewSet, base_name='products')
dashboard_router.register(r'categories', category_viewset.CategoryiewSet, base_name='categories')
dashboard_router.register(r'sellers', seller_viewset.SellerViewSet, base_name='categories')
dashboard_router.register(r'companies', company_viewset.CompanyViewSet, base_name='categories')
dashboard_router.register(r'orders', order_viewset.OrderViewSet, base_name='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/initial_data/', initial_data, name='initial_data'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('dashboard-api/', include(dashboard_router.urls)),

]
