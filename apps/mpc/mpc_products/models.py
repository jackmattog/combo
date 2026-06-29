from django.db import models
from django.utils.text import slugify

class MpcProductCategory(models.Model):
    mpc_product_category_name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="The unique name of the product category."
    )
    mpc_product_category_slug = models.SlugField(
        max_length=120, 
        unique=True, 
        blank=True,
        help_text="URL-friendly slug. Leaves blank to auto-generate from the name."
    )

    class Meta:
        verbose_name = "MPC Product Category"
        verbose_name_plural = "MPC Product Categories"
        ordering = ['mpc_product_category_name']

    def __str__(self):
        return self.mpc_product_category_name

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate 
        a slug from the category name if one isn't explicitly provided.
        """
        if not self.mpc_product_category_slug:
            self.mpc_product_category_slug = slugify(self.mpc_product_category_name)
        super().save(*args, **kwargs)