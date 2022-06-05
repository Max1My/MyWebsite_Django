from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductList, ProductCategoryList,BasketList, OrderList

router = DefaultRouter()
router.register('products',ProductList)
router.register('categories',ProductCategoryList)
router.register('basket',BasketList)
router.register('orders',OrderList)

urlpatterns = [
    path('',include(router.urls))
]