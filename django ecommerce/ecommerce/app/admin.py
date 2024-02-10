from django.contrib import admin
from .models import*
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discount_price','category','product_image']
    


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state']


    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.id])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)


    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','pay_order_id','pay_payment_status','pay_payment_id','paid']


    
@admin.register(OrderPlace)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']
    def customers(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    def products(self,obj):
        link=reverse('admin:app_product_change',args=[obj.product.id])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)    


    
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.id])
        return format_html('<a href="{}">{}</a>',link,obj.product.title),
