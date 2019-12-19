from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView

from accounting.models import Seller, User, Company
from dashboard.decorators import company_required, admin_required
from dashboard.forms import SellerCreateForm, CompanyCreateForm, ProductForm
from main.models import Product, Brand


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


class ProductListView(ListView):
    model = Product
    template_name = 'list.html'
    paginate_by = 20
    filter_list = ["brand"]

    def get_filters(self):
        filters = []
        filters.append({"title": "brand", "choices": Brand.objects.all()})
        return filters

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Product'
        data['field_list'] = ["title", "price", "brand"]
        data['filter_list'] = self.get_filters()
        return data

    # def get_queryset(self):


def product_list(request):
    products = Product.objects.all()
    return render(request, "classroom/product_list.html", {'products': products})


def product_view(request, pk, template_name='products/product_detail.html'):
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {'object': product})


def product_create(request, template_name='products/product_form.html'):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, template_name, {'form': form})


def product_update(request, pk, template_name='products/product_form.html'):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, template_name, {'form': form})


def product_delete(request, pk, template_name='products/product_confirm_delete.html'):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, template_name, {'object': product})
