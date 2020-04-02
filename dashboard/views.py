import django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django_filters.views import FilterView

from accounting.models import Seller, User, Company
from dashboard.decorators import company_required, admin_required
from dashboard.forms import SellerCreateForm, CompanyCreateForm, ProductForm
from main.models import Product


@login_required
@company_required
def dashboard(request):
    return render(request, 'classroom/home.html')


@login_required
@company_required
def seller_list(request):
    return render(request, 'classroom/seller_list.html', {"sellers": Seller.objects.all()})


@login_required
@admin_required
def company_list(request):
    return render(request, 'classroom/company_list.html', {"companies": Company.objects.all()})


class SellerCreateView(CreateView):
    model = User
    form_class = SellerCreateForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        seller = form.save()
        return redirect('dashboard')


class CompanyCreateView(CreateView):
    model = User
    form_class = CompanyCreateForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        company = form.save()
        return redirect('dashboard')


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {'brand': ['exact'], 'parent': ['exact'], 'existStatus': ['exact'], 'title': ["icontains"]}


class ProductListView(FilterView):
    model = Product
    template_name = 'list.html'
    paginate_by = 20
    filterset_class = ProductFilter

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Product'
        data['field_list'] = ["title", "price", "brand", "parent"]
        return data

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', None)
        if sort:
            queryset = queryset.order_by(sort)
        return queryset


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit.html'

    def form_valid(self, form):
        product = form.save()
        return redirect('dashboard')
