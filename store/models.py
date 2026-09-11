from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('children', 'Children'),
        ('bags', 'Bags'),
        ('shoes', 'Shoes'),
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sale_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True
)

    image = models.ImageField(
        upload_to='products/'
    )

    description = models.TextField()

    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# =========================
# CART MODEL
# =========================

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    # =========================
# ADDRESS MODEL
# =========================

class Address(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"

    # =========================
# ORDER MODEL
# =========================

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# =========================
# ORDER ITEM MODEL
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product} - {self.quantity}"