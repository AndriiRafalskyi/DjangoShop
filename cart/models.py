from django.db import models
from store.models import Product, Variation

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def get_item_with_same_variations(items, variations):
        for item in items:
            if list(item.variations.all()) == variations:
                return item
        return None

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
