from django.db import models
from django.contrib.auth.models import User

# Create your models here.


CATEGORY_CHOICES = (
    ('tshirt','tshirt'),
    ('wintertshirt','wintertshirt'),
    ('summertshirt','summertshirt'),
    ('winterjacket','winterjacket'),
    ('dailyshoes','dailyshoes'),
    ('jeans','jeans'),
)


STATE_CHOICES=( 
    ('Adana','Adana'),
    ('Adiyaman','Adiyaman'),
    ('Afyon','Afyon'),
    ('Ağrı','Ağrı'),
    ('Amasya','Amasya'),
    ('Ankara','Ankara'),
    ('Antalya','Antalya'),
    ('Artvin','Artvin'),
    ('Aydın','Aydın'),
    ('Balıkesir','Balıkesir'),
    ('Bilecik','Bilecik'),
    ('Bingöl','Bingöl'),
    ('Bitlis','Bitlis'),
    ('Bolu','Bolu'),
    ('Burdur','Burdur'),
    ('Bursa','Bursa'),
    ('Çanakkale','Çanakkale'),
    ('Çankırı','Çankırı'),
    ('Çorum','Çorum'),
    ('Denizli','Denizli'),
    ('Diyarbakır','Diyarbakır'),
    ('Edirne','Edirne'),
    ('Elazığ','Elazığ'),
    ('Erzincan','Erzincan'),
    ('Erzurum','Erzurum'),
    ('Eskişehir','Eskişehir'),
    ('Gaziantep','Gaziantep'),
    ('Giresun','Giresun'),
    ('Gümüşhane','Gümüşhane'),
    ('Hakkari','Hakkari'),
    ('Hatay','Hatay'),
    ('Isparta','Isparta'),
    ('Mersin','Mersin'),
    ('İstanbul','İstanbul'),
    ('İzmir','İzmir'),
    ('Kars','Kars'),
    ('Kastamonu','Kastamonu'),
    ('Kars','Kars'),
    ('Kırklareli','Kırklareli'),
    ('Eskişehir','Eskişehir'),
    ('Kocaeli','Kocaeli'),
    ('Konya','Konya'),
    ('Kütahya','Kütahya'),
    ('Malatya','Malatya'),
    ('Manisa','Manisa'),
    ('Kahramanmaraş','Kahramanmaraş'),
    ('Mardin','Mardin'),
    ('Muğla','Muğla'),
    ('Muş','Muş'),
    ('Nevşehir','Nevşehir'),
    ('Niğde','Niğde'),
    ('Ordu','Ordu'),
    ('Rize','Rize'),
    ('Sakarya','Sakarya'),
    ('Samsun','Samsun'),
    ('Siirt','Siirt'),
    ('Sinop','Sinop'),
    ('Sivas','Sivas'),
    ('Tekirdağ','Tekirdağ'),
    ('Tokat','Tokat'),
    ('Trabzon','Trabzon'),
    ('Tunceli','Tunceli'),
    ('Şanlıurfa','Şanlıurfa'),
    ('Uşak','Uşak'),
    ('Van','Van'),
    ('Yozgat','Yozgat'),
    ('Zonguldak','Zonguldak'),
    ('Aksaray','Aksaray'),
    ('Bayburt','Bayburt'),
    ('Karaman','Karaman'),
    ('Kırkkale','Kırıkkale'),
    ('Batman','batman'),
    ('Şırnak','Şırnak'),
    ('Bartın','Bartın'),
    ('Ardahan','Ardahan'),
    ('Iğdır','Iğdır'),
    ('Yalova','Yalova'),
    ('Karabük','Karabük'),
    ('Kilis','Kilis'),
    ('Osmaniye','Osmaniye'),
    ('Düzce','Düzce'),

)


class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField(max_length=250)
    composition = models.TextField(default ='')
    prodapp = models.TextField(default='')
    
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=25)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)
    
    
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    pay_order_id = models.CharField(max_length=250,blank=True,null=True)
    pay_payment_status = models.CharField(max_length=250,blank=True,null=True)
    pay_payment_id = models.CharField(max_length=250,blank=True,null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlace(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250,choices=STATUS_CHOICES,default='pending')
    payment =models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)