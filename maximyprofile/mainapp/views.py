import random

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:6]
    return same_products


def main(request):
    menu = [
        {'href': '', 'name': 'главная'},
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
    ]
    hot_product = get_hot_products()
    same_products = get_same_products(hot_product)
    products = Product.objects.all().order_by('-id')[:6]

    content = {
        "title": 'Магазин',
        'menu': menu,
        'hot_product': hot_product,
        "same_products": same_products,
        "products" : products,
    }
    return render(request, 'mainapp/index.html', content)

def computers(request):

    return render(request,'mainapp/computers.html')

def products(request, pk=None,page=1):
    print(pk)
    title = "Продукты"
    links_menu = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)


    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name':'все'}
        else:
            category = get_object_or_404(ProductCategory,pk=pk)
            products = Product.objects.filter(category__pk=pk,is_active=True).order_by('price')

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

    hot_product = get_hot_products()
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

    content = {
        'title':title,
        'links_menu':ProductCategory.objects.all(),
        'product':get_object_or_404(Product, pk=pk),
        'basket':get_basket(request.user),
        'menu':menu,
    }

    return render(request,'mainapp/product.html', content)

def products_list(request):
    return render(request,'mainapp/products_list.html')
