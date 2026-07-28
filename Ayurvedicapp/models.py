from django.db import models
from django.utils import timezone
import datetime



# Create your models here.


class tbl_register(models.Model):
    email=models.EmailField(max_length=100,default="")
    phn=models.CharField(max_length=100,default="")
    name=models.CharField(max_length=100,default="")
    uname=models.CharField(max_length=100,default="")
    pswd=models.CharField(max_length=100,default="")
    adrs=models.CharField(max_length=100,default="")
    utype=models.CharField(max_length=100,default="")

class tbl_doctor(models.Model):
    email = models.EmailField(max_length=100, default="")
    phn = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")
    uname = models.CharField(max_length=100, default="")
    pswd = models.CharField(max_length=100, default="")
    adrs = models.CharField(max_length=100, default="")
    available_time = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, default="")
    utype = models.CharField(max_length=100, default="")
    profile_image = models.ImageField(upload_to='doctor_profile', default='default_pro.png')


class tbl_message(models.Model):    
    msg = models.TextField(default='')
    file=models.ImageField(upload_to='file',default='null.jpeg')
    user_id=models.ForeignKey(tbl_register,on_delete=models.CASCADE, blank=True,null=True)
    doctor_id=models.ForeignKey(tbl_doctor,on_delete=models.CASCADE, blank=True,null=True)
    utype=models.CharField(max_length=100,default="")
    


class tbl_shopdetails(models.Model):
    lname=models.CharField(max_length=100,default="")   #labour name
    phn=models.CharField(max_length=100,default="")
    adrs=models.CharField(max_length=100,default="")
    pname=models.CharField(max_length=100,default="")   #product name
    amnt=models.CharField(max_length=100,default="")
    qnty=models.CharField(max_length=100,default="")
    files=models.ImageField(upload_to='file',default='null.jpeg')
    img=models.ImageField(upload_to='file',default='null.jpeg')
    status=models.CharField(max_length=100,default="")
    description=models.TextField(default="")
    shop_id=models.ForeignKey(tbl_register,on_delete=models.CASCADE, blank=True,null=True)



class tb_cart(models.Model):
    qnty = models.CharField(max_length=100, default='')
    date = models.CharField(max_length=100, default='')
    total_price = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='')
    product_id = models.ForeignKey( tbl_shopdetails, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)


class tbl_order(models.Model):
    user_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE,blank=True, null=True)
    cart_id = models.ForeignKey(tb_cart, on_delete=models.CASCADE,blank=True, null=True)
    product_id = models.ForeignKey(tbl_shopdetails, on_delete=models.CASCADE,blank=True, null=True)
    total = models.CharField(max_length=30, default='')
    date = models.CharField(max_length=100, default='')
    time = models.CharField(max_length=100, default='')
    payment_status = models.CharField(max_length=30, default='')
    order_id = models.CharField(max_length=100, default='')
    order_status = models.CharField(max_length=100, default='pending')



class tbl_payment(models.Model):
    user_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE,blank=True, null=True)
    # product_id = models.ForeignKey(tbl_shopdetails, on_delete=models.CASCADE,blank=True, null=True)
    order_id = models.ForeignKey(tbl_order, on_delete=models.CASCADE,blank=True, null=True)
    date = models.CharField(max_length=100, default='')
    total_amt = models.CharField(max_length=100, default='')
    card_name = models.CharField(max_length=100, default='')
    card_number = models.CharField(max_length=100, default='')
    card_date = models.CharField(max_length=100, default='')
    card_cvv = models.CharField(max_length=100, default='')
    card_expdate = models.CharField(max_length=100, default='')
    pay_status = models.CharField(max_length=100, default='')

    
class tbl_booking(models.Model):
    user_id=models.ForeignKey(tbl_register, on_delete=models.CASCADE,blank=True, null=True)
    doctor_id=doctor_id=models.ForeignKey(tbl_doctor,on_delete=models.CASCADE, blank=True,null=True)
    time=models.CharField(max_length=100, default='')
    date=models.CharField(max_length=100, default='')
    status=models.CharField(max_length=100, default='')
    doctor_status=models.CharField(max_length=100, default='')



class tbl_feedback(models.Model):
    user_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True, related_name='user_feedback')
    product_id = models.ForeignKey(tbl_shopdetails, on_delete=models.CASCADE, blank=True, null=True, related_name='product_feedback')
    shop_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True, related_name='shop_feedback')
    msg = models.TextField(default='')


class tbl_review(models.Model):
    user_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    doctor_id = models.ForeignKey(tbl_doctor, on_delete=models.CASCADE, blank=True, null=True)
    msg = models.TextField(default='')


class tbl_chat(models.Model):    
    message = models.TextField(default='')
    sender=models.ForeignKey(tbl_register,on_delete=models.CASCADE, blank=True,null=True)
    receiver=models.ForeignKey(tbl_doctor,on_delete=models.CASCADE, blank=True,null=True)
    utype=models.CharField(max_length=100,default="")
    time = models.CharField(max_length=100,default="")
    
class tbl_notifications(models.Model):
    user_id = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    utype=models.CharField(max_length=100,default="")

class tbl_doctor_notifications(models.Model):
    user_id = models.ForeignKey(tbl_doctor, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    utype=models.CharField(max_length=100,default="")
    
