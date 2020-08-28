from django.contrib import admin
from shop.models import Product, Contact, Orders, OrderItems, UserInfo, Payment


admin.site.site_title = 'E-commerce'
admin.site.site_header = 'E-commerce Administration'


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id','name','email')
    list_filter = ('email',)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product', 'order_status')
    list_filter = ('order_id', 'order_id__order_status')



# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(UserInfo)
admin.site.register(Payment)
