import hashlib
import random
from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUserRegisterForm, ShopUserProfileForm
from mainapp.models import ProductCategory, Product
from django.forms import Form, HiddenInput,ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django.core.exceptions import ValidationError




class ShopUserAdminRegisterForm(ShopUserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ShopUserAdminRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

class ShopUserAdminProfileForm(ShopUserProfileForm):
    email = forms.EmailField(widget=forms.EmailInput())
    username = forms.CharField(widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(ShopUserAdminProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['readonly'] = False
        self.fields['username'].widget.attrs['readonly'] = False
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(ProductCategoryEditForm).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''
                if field_name == 'password':
                    field.widget = HiddenInput()

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(ProductEditForm).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''

# class ProductRegisterForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = "__all__"
#
#     def __init__(self, *args, **kwargs):
#         super(ProductRegisterForm).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''
class ProductCategoryUpdateFormAdmin(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput())
    # description = forms.CharField(widget=forms.TextInput(), required=False)
    # # is_active = forms.BooleanField(widget=forms.CheckboxInput())
    discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=90,initial=0)


    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(ProductCategoryUpdateFormAdmin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

class ProductsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all())
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

class ProductUpdate(ProductsForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all().select_related(),
                                      empty_label=None)
    image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'