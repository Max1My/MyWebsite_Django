from mainapp.models import Product,ProductCategory
from basketapp.models import Basket
from ordersapp.models import Order
from rest_framework import serializers


class ProductList(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','quantity')

class ProductCategoryList(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id','name')

class BasketList(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user','product','quantity')

class OrderList(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','user','status')