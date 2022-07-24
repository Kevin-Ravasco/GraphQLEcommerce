from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from products.models import Category, Product


@receiver(pre_save, sender=Category, dispatch_uid="create_category_slug")
def create_category_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Product, dispatch_uid="create_product_slug")
def create_product_slug(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    instance.slug = f"{slug}-{instance.id}"
