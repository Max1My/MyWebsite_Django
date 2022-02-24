from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp.views import products, product,products_ajax,contacts,sitemap

app_name = 'mainapp'

urlpatterns = [
   path('', products, name='index'),
   path('category/<int:pk>/', products, name='category'),
   path('category/<int:pk>/$', cache_page(3600)(products),name='category'),
   path('category/<int:pk>/ajax/$',cache_page(3600)(products_ajax)),
   path('category/<int:pk>/page/<int:page>/', products, name='page'),
   path('category/<int:pk>/page/<int:page>/ajax/$',cache_page(3600)(products_ajax)),
   path('product/<int:pk>/',product, name='product'),
]

# urlpatterns = [
#
#     path('', products,name='index'),
#     path('category/<int:id_category>/', products, name='category'),
#     path('category/<int:id_category>/page/<int:page>/', products, name='page'),
#     path('product/<int:pk>/', ProductDetail.as_view(), name='product'),
#
# ]