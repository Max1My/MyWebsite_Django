from rest_framework.viewsets import ModelViewSet
from mainapp.models import Product,ProductCategory
from basketapp.models import Basket
from ordersapp.models import Order
from api.serializers import ProductList,ProductCategoryList, BasketList, OrderList


class ProductList(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductList

class ProductCategoryList(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryList

class BasketList(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketList

class OrderList(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderList