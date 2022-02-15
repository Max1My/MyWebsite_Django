import random

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import ProductCategory, Product
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string
from django.http import JsonResponse
import random

# links_menu = [
#     {'href': 'products_all', 'name': 'все'},
#     {'href': 'products_computers', 'name': 'Компьютеры'},
#     {'href': 'products_smartphones', 'name': 'Смартфоны'},
menu = [
        {'href': '', 'name': 'главная'},
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
]


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []



def get_hot_products():
    products = Product.objects.all()

    return random.sample(list(products), 6)[0]

def get_hot_product():
    products = get_products()

    return random.sample(list(products),6)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:6]
    return same_products


def main(request):
    menu = [
        {'href': '', 'name': 'главная'},
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
    ]
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    products = get_products()[:6]

    content = {
        "title": 'Магазин',
        'menu': menu,
        'hot_product': hot_product,
        "same_products": same_products,
        "products" : products,
        'links_menu':ProductCategory.objects.all()
    }
    return render(request, 'mainapp/index.html', content)

def computers(request):

    return render(request,'mainapp/computers.html')

def contacts(request):
    title = 'Контакты'
    links_menu = get_links_menu()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        "title": title,
        'hot_product': hot_product,
        "same_products": same_products,
        "menu": menu,
    }

    return render(request,'mainapp/contacts.html',content)

def sitemap(request):

    return render(request,'mainapp/sitemap.html')

def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.all()
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
   if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
       if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
       return category
   else:
       return get_object_or_404(ProductCategory, pk=pk)

def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).order_by('price')
            cache.set(key,products)
        return products
    else:
        return Product.objects.filter(is_active=True).order_by('price')

def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category=pk, is_active=True).order_by('price')
            cache.set(key,products)
        return products
    else:
        Product.objects.filter(category__pk=pk, is_active=True).order_by('price')

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).select_related('category')



# def get_link_category():
#     if settings.LOW_CACHE:
#         key = 'link_category'
#         link_category = cache.get(key)
#         if link_category is None:
#             ProductCategory.objects.all()
#             cache.set(key,link_category)
#         return link_category
#     else:
#         return ProductCategory.objects.all()


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

def products_ajax(request,pk=None,page=1):
    if request.is_ajax():
        links_menu = get_links_menu()

        if pk:
            if pk == '0':
                category = {
                    'pk': 0,
                    'name': 'все',
                }
                products = get_products_ordered_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_ordered_by_price(pk)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                        'mainapp/includes/inc_products_list_content.html',
                        context=content,
                        request=request)

            return JsonResponse({'result': result})


# @cache_page(3600)
def products(request, pk=None,page=1):
    print(pk)
    title = "Продукты"
    links_menu = get_links_menu()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = get_products_ordered_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        pagintor = Paginator(products, 2)

        try:
            products_paginator = pagintor.page(page)
        except PageNotAnInteger:
            products_paginator = pagintor.page(1)
        except EmptyPage:
            products_paginator = pagintor.page(pagintor.num_pages)

        content = {
            "title":title,
            'links_menu':links_menu,
            "category":category,
            "menu":menu,
            'products':products_paginator,
            'basket':basket,
        }
        return render(request,'mainapp/products_list.html',content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)


    content = {
        "title": title,
        'links_menu': links_menu,
        'hot_product':hot_product,
        "same_products": same_products,
        "menu": menu,
        'basket':basket,
    }

    return render(request,'mainapp/products.html',content)

def product(request,pk):
    title = 'продукты'
    product = get_product(pk)

    content = {
        'title':title,
        'links_menu':ProductCategory.objects.all(),
        'product':product,
        'basket':get_basket(request.user),
        'menu':menu,
    }

    return render(request,'mainapp/product.html', content)

# class ProductDetail(DetailView):
#     """
#     Контроллер вывода информации о продукте
#     """
#     model = Product
#     template_name = 'mainapp/product.html'