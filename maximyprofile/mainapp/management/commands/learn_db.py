from django.core.management.base import BaseCommand
from mainapp.models import Product
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        # ИЛИ
        # products = Product.objects.filter(
        #     Q(category__name='Смартфоны') | Q(pk=2))

        # И
        # products = Product.objects.filter(
        #     Q(category__name='Смартфоны') & Q(id=13)
        # )

        # НЕ
        # products = Product.objects.filter(
        #     ~Q(category__name='Смартфоны')
        # )
        # И НЕ
        products = Product.objects.filter(
            ~Q(category__name='Смартфоны'), id=10
        )

        print(products)