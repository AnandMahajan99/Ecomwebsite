from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Booked', 'Booked'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)

PAYMENT_STATUS = (
    ('Success', 'Success'),
    ('Failure', 'Failure'),
    ('Pending', 'Pending')
)

class UserInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional information
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def order(self):
        return self.user_order.all()

class Product(models.Model):
    """
    Model for storing product details
    """
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=30, default="")
    sub_category = models.CharField(max_length=30, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images/", default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    """
    Model for storing contact details if someone want to contact
    """
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=12, default="")
    desc = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

class Orders(models.Model):
    """
    Model for storing customer order details
    """
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, related_name="user_order", on_delete=models.CASCADE)
    # items = models.CharField(max_length=500)
    no_of_items = models.IntegerField(default=0)
    order_status = models.CharField(max_length=12, choices=ORDER_STATUS, default='Pending')
    total_price = models.IntegerField(default=0)
    pub_date_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=70)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=10, validators=[RegexValidator('^[6-9]{1}[0-9]{9}$','Enter a valid mobile number')])

    def __str__(self):
        return str(self.order_id)

    def order_items(self):
        return self.order.all()

class OrderItems(models.Model):
    order_id = models.ForeignKey(Orders, related_name='order', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.order_id)

    def order_status(self):
        return self.order_id.order_status

    def product(self):
        name = self.product_id.product_name
        id = self.product_id_id
        # print(id)
        url = reverse('Products', kwargs={'myid':id})
        return format_html('<a href='+ url +'>'+ name +'</a>')


# class Cart

class Payment(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    txn_id = models.CharField(max_length=100)
    bank_txn_id = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=12, choices=PAYMENT_STATUS)
    payment_date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.txn_id

    def change_order_status(self):
        if self.payment_status == 'Success':
            order = Orders.objects.get(order_id = str(self.order_id))
            order.order_status = 'Booked'
            order.save()
            print(order.order_status)
        elif self.payment_status == 'Failure':
            order = Orders.objects.get(order_id=str(self.order_id))
            order.order_status = 'Cancel'
            order.save()
            print(order.order_status)


# class Category
