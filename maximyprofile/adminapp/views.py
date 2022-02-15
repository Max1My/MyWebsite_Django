from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ProductCategoryEditForm, ProductEditForm ,ShopUserAdminRegisterForm , ShopUserAdminProfileForm,ProductCategoryUpdateFormAdmin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin

class IndexTemplateView(TemplateView):
    template_name = 'adminapp/admin.html'

# Users
class UsersListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/users.html'
    title = 'Админка | Пользователи'


class UserCreateView(CreateView,BaseClassContextMixin,CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    form_class = ShopUserAdminRegisterForm
    success_url = reverse_lazy('adminapp:users')
    title = 'Админка | Создание пользователя'

class UserUpdateView(UpdateView,BaseClassContextMixin,CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminProfileForm
    success_url = reverse_lazy('adminapp:users_update')
    title = 'Админка | Обновить пользователя'


class UserDeleteView(DeleteView,BaseClassContextMixin,CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    form_class = ShopUserAdminProfileForm
    success_url = reverse_lazy('admins:users_delete')
    title = 'Админка | Удалить пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse('admins:users'))

# Category
class ProductCategoryListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    title = 'Админка | Список категорий'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admins:categories')
    form_class = ProductCategoryUpdateFormAdmin
    title = 'Админка | Создание категории'


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update_delete.html'
    form_class = ProductCategoryUpdateFormAdmin
    title = 'Админка | Обновление категории'
    success_url = reverse_lazy('admins:categories')


class ProductCategoryDeleteView(DeleteView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/category_update_delete.html'
    success_url = reverse_lazy('admins:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

# Products
class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admins:products')
    fields = '__all__'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admins:products')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/редактирование'

        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admins:products')
    fields = '__all__'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
