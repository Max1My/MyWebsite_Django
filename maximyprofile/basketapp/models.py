from django.db import models
from django.conf import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(BasketQuerySet,self).delete(*args,**kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()

    def save(self,*args,**kwargs):
        if self.pk:
            get_item = self.get_item(int(self.pk))
            self.product.quantity -= self.quantity - get_item
        else:
            self.product.quantity -= self.quantity

        self.product.save()
        super(Basket,self).save(*args,**kwargs)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity