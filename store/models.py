from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_extensions.db.fields import ShortUUIDField

# Create your models here.

def get_cat_image_folder(instance, filename):
    category = instance.product.category.category
    cat = category.replace(" ","_")
    filename = instance.product.name
    file_name = filename.replace(" ","_")
    try:
        if instance.main_image:
            file_name += '_main.jpg'
    except:
        file_name += '_extra.jpg'

    return '{0}/{1}'.format(cat, file_name)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class ShippingFrom(models.Model):
    city = models.CharField(max_length=200, null=True)
    kecamatan = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'Shipping from: '+self.city

class ProductColor(models.Model):
    color_name = models.CharField(max_length=20, null=True)
    color_hex = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.color_name


class ProductSize(models.Model):
    size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return 'Size: '+self.size


class ProductCategory(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.category


class Product(models.Model):
    product_id = ShortUUIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    shipping_from = models.ForeignKey(ShippingFrom, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(blank=True)
    variation = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to=get_cat_image_folder,)
    main_image = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product.name)+' '+str(self.description)


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product.name


# class ProductMainImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     main_image = models.ImageField(upload_to=get_cat_image_folder,)
#
#     def __str__(self):
#         return self.product.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    def __str__(self):
        return 'Customer: '+self.customer.name+', Transaction completed? '+str(self.complete)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product_variation:
            total = self.product_variation.price * self.quantity
        else:
            total = self.product.price * self.quantity

        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=400, null=True)
    city = models.CharField(max_length=200, null=True)
    kecamatan = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
