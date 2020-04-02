from django.urls import path, include

from dashboard.views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('sellers/create', SellerCreateView.as_view(), name="create_seller"),
    path('sellers', seller_list, name="sellers"),
    path('companies/create', CompanyCreateView.as_view(), name="create_company"),
    path('companies', company_list, name="companies"),

    path('products/', ProductListView.as_view(), name='product_list'),
    # path('products/view/<int:pk>',product_view, name='product_view'),
    path('products/create', ProductCreateView.as_view(), name='product_new'),
    # path('products/edit/<int:pk>', product_update, name='product_edit'),
    # path('products/delete/<int:pk>', product_delete, name='product_delete'),
    # path('product/', include(ProductView().get_urls()))
]
