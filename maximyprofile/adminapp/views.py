from django.db.models import F
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ProductCategoryEditForm, ProductEditForm, ShopUserAdminRegisterForm, \
    ShopUserAdminProfileForm, ProductCategoryUpdateFormAdmin, ProductsForm
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView
from django.db import connection
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin


class IndexTemplateView(TemplateView):
    template_name = 'adminapp/admin.html'


# Users
class UsersListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/users.html'
    title = 'Админка | Пользователи'


class UserCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    form_class = ShopUserAdminRegisterForm
    success_url = reverse_lazy('adminapp:users')
    title = 'Админка | Создание пользователя'


class UserUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminProfileForm
    success_url = reverse_lazy('adminapp:users_update')
    title = 'Админка | Обновить пользователя'


class UserDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
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
class ProductCategoryListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
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

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                self.db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return HttpResponseRedirect(self.get_success_url())

    def db_profile_by_type(self, prefix, type, queries):
        update_queries = list(filter(lambda x: type in x['sql'], queries))
        print(f'db_profile {type} for {prefix}:')
        [print(query['sql']) for query in update_queries]


class ProductCategoryDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/category_update_delete.html'
    success_url = reverse_lazy('admins:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.product_set.update(is_active=False)
        # self.object.is_active = False if self.object.is_active else True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# Products

class ProductListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/products.html'
    title = 'Админка | Обновления категории'


@user_passes_test(lambda u: u.is_superuser)
def products_category(request, pk):
    title = 'админка/продукты'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products_category.html', content)


class ProductUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/product_update_delete.html'
    form_class = ProductsForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('adminapp:products')


class ProductCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/product_create.html'
    form_class = ProductsForm
    title = 'Админка | Создание продукта'
    success_url = reverse_lazy('admins:products')


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admins:products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # self.object.is_active = False if self.object.is_active else True
        # self.object.save()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
