"""maximyprofile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path
import mainapp.views as mainapp
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import debug_toolbar
from django.conf import settings
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admins/',include('adminapp.urls',namespace='admins')),
    path('',mainapp.main,name='index'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    # path('products_list/', mainapp.products_list, name='products_list'),
    path('basket/',include('basketapp.urls', namespace='basket')),
    path('product/',include('mainapp.urls',namespace='product')),
    path('',include('social_django.urls',namespace='social')),
    path('orders/',include('ordersapp.urls',namespace='orders')),
    path('contacts/',mainapp.contacts,name='contacts'),
    path('sitemap/',mainapp.sitemap,name='sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('debug/',include(debug_toolbar.urls))]