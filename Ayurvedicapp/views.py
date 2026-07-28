from django.shortcuts import render,redirect
from.models import*
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from datetime import date
import uuid
# Create your views here.


def index(request):
    return render(request,'index.html')


def user_reg(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        tbl_register(name=name,uname=uname,email=email,pswd=pswd,adrs=adrs,phn=phn,utype='user').save()
        return render(request,'index.html')
    else:
        return render(request,'user_reg.html')
    



def shop_reg(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        tbl_register(name=name,uname=uname,email=email,pswd=pswd,adrs=adrs,phn=phn,utype='shop').save()
        return render(request,'index.html')
    else:
        return render(request,'shop_reg.html')
    

    


def login(request):
    if request.method == "POST":
        pswd = request.POST['pswd']
        email = request.POST['email']
        var = tbl_register.objects.all().filter(pswd=pswd, email=email, utype='user')
        var2 = tbl_register.objects.all().filter(pswd=pswd, email=email, utype='shop')
        var3 = tbl_doctor.objects.all().filter(pswd=pswd, email=email, utype='doctor')
        var4= tbl_register.objects.all().filter(pswd=pswd, email=email, utype='admin')

        if var:
            for x in var:
                request.session['id'] = x.id
            return render(request, 'user/user_home.html')
        if var2:
            for x in var2:
                request.session['id'] = x.id
            return render(request, 'shop/shop_home.html')
        elif var3:
            for x in var3:
                request.session['id'] = x.id
            return render(request, 'doctor/doctor_home.html')
        
        elif var4:
            for x in var4:
                request.session['id'] = x.id
            return render(request, 'admin/admin_home.html')

        else:
            txt = """<script>alert("Invalid user Credentials....");window.location='/';</script>"""
            return HttpResponse(txt) 
    else:
        return render(request, "login.html")
    


def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return render(request,'index.html')





    
    # .........................user...................


    
def user_home(request):
    return render(request,'user/user_home.html')


def user_profile(request):
    id=request.session['id']
    data=tbl_register.objects.all().filter(id=id)
    return render(request,'user/user_profile.html',{'data':data}) 


def user_editprofile(request,id):
    if request.method == "POST":
        email = request.POST.get('email') 
        phn = request.POST.get('phn')
        name = request.POST.get('name')
        uname = request.POST.get('uname')      
        pswd = request.POST.get('pswd')   
        adrs = request.POST.get('adrs') 
        tbl_register.objects.all().filter(id=id).update(email=email, phn=phn, name=name,uname=uname,pswd=pswd,adrs=adrs)   
        return redirect('user_profile')  
    else:
        data=tbl_register.objects.all().filter(id=id)
        return render(request, 'user/user_editprofile.html',{'data': data})



def user_view_doctor(request):
    data=tbl_doctor.objects.all()
    return render(request,'user/user_view_doctor.html',{'data':data}) 



def user_add_message(request,id):
    if request.method == 'POST':
        user_id = request.session['id']
        doctor_id = request.POST.get('doctor_id')
        user_instance = tbl_register.objects.get(id=user_id)
        doctor_instance = tbl_doctor.objects.get(id=doctor_id)
        msg = request.POST.get('msg')
        file= request.FILES.get('file')
        tbl_message(user_id=user_instance, doctor_id=doctor_instance, msg=msg,file=file,utype='user').save()
        return render(request, 'user/user_home.html')
    else:
        data = tbl_doctor.objects.get(id=id)
        return render(request, 'user/user_add_message.html', {'data': data})





def user_view_DoctorMessage(request):
    user_id = request.session.get('id')
    var = tbl_message.objects.filter(user_id=user_id,utype='doctor').select_related('doctor_id','user_id')
    return render(request, 'user/user_view_DoctorMessage.html', {"var": var})


def user_view_notifications(request):
    user_id = request.session.get('id')
    notifications = tbl_notifications.objects.filter(user_id=user_id , utype="user").order_by('-timestamp')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'user/user_view_notifications.html', context)


def shop_view_notifications(request):
    user_id = request.session.get('id')
    notifications = tbl_notifications.objects.filter(user_id=user_id , utype="shop").order_by('-timestamp')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'shop/shop_view_notifications.html', context)


def user_view_shops(request):
    data = tbl_shopdetails.objects.all().filter(status='approved').select_related('shop_id')
    return render(request, "user/user_view_shops.html", {'data': data})





def user_view_product(request):
    id=request.GET['id']
    data=tbl_shopdetails.objects.all().filter(id=id)
    return render(request,'user/user_view_product.html',{'data':data})



def user_view_product_details(request):
    id=request.GET['id']
    data=tbl_shopdetails.objects.all().filter(id=id)
    print('data',data)
    return render(request,'user/user_view_product_details.html',{'data':data})



def add_to_cart(request):
    myid = request.session['id']
    ii = request.GET['id']
    pid = tbl_shopdetails.objects.get(id=ii)
    uid = tbl_register.objects.get(id=myid)
    number = request.GET['number']
    date = datetime.date.today()
    aq = int(pid.qnty)
    qu = int(number)
    if(aq < qu):
         error_message = "Requested Quantity is Not Available"
         print('....',error_message)
         return render(request, 'user/user_view_product_details.html', {'error': error_message})
    else:
        proprice = (pid.amnt)
        total = int(proprice)*int(number)
        tb_cart(qnty=number, user_id=uid, status='pending',date=date, product_id=pid, total_price=total).save()
        new_qty = int(pid.qnty)-int(number)
        tbl_shopdetails.objects.all().filter(id=(pid.id)).update(qnty=new_qty)
        shid = (pid.shop_id.id)
        return HttpResponseRedirect('/user_cartpage/')




def user_cartpage(request):
    myid = request.session['id']
    var = tb_cart.objects.all().filter(user_id=myid, status='pending')
    sum1 = 0
    for x in var:
        a = x.total_price
        sum1 = sum1+int(a)
        print(sum1)
    return render(request, 'user/user_cartpage.html', {'var': var, 'sum': sum1})





from django.db.models import F
def delete_cart(request):
    try:
        ii = request.GET['id']
        # Retrieve cart item details
        cart_item = tb_cart.objects.get(id=ii)
        product_id = cart_item.product_id
        quantity_to_add = int(cart_item.qnty)
        # Delete the cart item
        cart_item.delete()
        # Update the quantity in tbl_shopdetails
        tbl_shopdetails.objects.filter(id=product_id.id).update(qnty=F('qnty') + quantity_to_add)
        return HttpResponseRedirect('/user_cartpage/')
    except tb_cart.DoesNotExist:
        # Handle the case where the cart item does not exist
        error_message = "Cart item not found"
        print('....', error_message)
        return render(request, 'user/user_cartpage.html', {'error': error_message})





def cart_product_payment(request):
    if request.method == 'POST':
         user_id=request.session.get('id')
         product_id = request.POST.get('product_id')
         cart_id= request.POST.get('cart_id')
         if not product_id or not cart_id:
            error_message = "Your Cart Is Empty"
            return render(request, 'user/user_cartpage.html', {'error': error_message})
         amount = request.POST["subtotal"]
         current_date = date.today()
         now = datetime.datetime.now()
         current_time = now.strftime("%H:%M:%S")
         uid=tbl_register.objects.get(id=user_id)
         cid=tb_cart.objects.get(id=cart_id)
         pids =  request.POST.getlist('product_id')
         for product_id in pids:
            pid=tbl_shopdetails.objects.get(id=product_id)
            order_id = int(uuid.uuid4().int)
            tbl_order(cart_id=cid,user_id=uid, product_id=pid,date=current_date,time=current_time,total=amount,payment_status='pending',order_id=order_id).save()
         return render(request,'user/user_payment.html',{"order_id":order_id})
    else:
        return render(request, 'user/user_payment.html')
    



def user_payment(request):
    if request.method == 'POST':
        user_id = request.session.get('id')
        order_id = request.POST.get('order_id')
        cardname = request.POST['cardname']
        cardnumber = request.POST['cardnumber']
        carddate = request.POST['carddate']
        cardcvv = request.POST['cardcvv']

        # Get user and order objects
        user_obj = tbl_register.objects.get(id=user_id)
        order_obj = tbl_order.objects.get(order_id=order_id)

        # Create a payment record
        tbl_payment.objects.create(
            order_id=order_obj,
            user_id=user_obj,
            card_cvv=cardcvv,
            card_date=carddate,
            card_number=cardnumber,
            card_name=cardname,
            pay_status='paid'
        )

        # Update cart and order statuses
        tb_cart.objects.filter(user_id=user_obj).update(status='paid')
        tbl_order.objects.filter(user_id=user_obj).update(payment_status='paid')

        # Add a shop notification
        shop_obj = tbl_register.objects.get(id=order_obj.product_id.shop_id.id)
        shop_notification_message = f"New order with ID {order_obj.id} has been placed and the payment is completed."

        tbl_notifications.objects.create(
            user_id=shop_obj,
            message=shop_notification_message,
            utype='shop'
        )
        return render(request, 'user/user_home.html')
    else:
        order_id = request.POST.get('order_id')
        data1 = tbl_order.objects.filter(order_id=order_id)
        return render(request, 'user/user_payment.html', {'data1': data1})
    


def user_orders(request):
    user_id = request.session.get('id')
    data = tbl_order.objects.filter(user_id=user_id, payment_status='paid').select_related('product_id', 'cart_id')
    return render(request, 'user/user_orders.html', {'data': data})



def user_booking_doctor(request):
    if request.method == 'POST':
        user_id = request.session['id']
        doctor_id = request.POST.get('doctor_id') 
        date = request.POST.get('date')
        time = request.POST.get('time')
        uid = tbl_register.objects.get(id=user_id)
        did = tbl_doctor.objects.get(id=doctor_id)
        tbl_booking(user_id=uid, doctor_id=did, date=date, time=time, status='pending',doctor_status='pending').save()
        return render(request, 'user/user_home.html')
    else:
        id=request.GET['id']
        data = tbl_doctor.objects.get(id=id)
        return render(request, 'user/user_booking_doctor.html', {'data': data})

    

def user_view_doctor_confirmation(request):
    user_id = request.session.get('id')
    data= tbl_booking.objects.all().filter(user_id=user_id,doctor_status='confirmed').select_related('doctor_id')
    return render(request,'user/user_view_doctor_confirmation.html',{'data':data})



def user_add_feedback(request):
    if request.method == 'POST':
        user_id = request.session['id']
        product_id = request.POST.get('product_id') 
        shop_id = request.POST.get('shop_id') 
        msg = request.POST.get('msg')
        uid = tbl_register.objects.get(id=user_id)
        pid = tbl_shopdetails.objects.get(id=product_id)
        sid = tbl_register.objects.get(id=shop_id)
        tbl_feedback(user_id=uid, product_id=pid,shop_id=sid,msg=msg).save()
        return render(request, 'user/user_home.html')
    else:
        id=request.GET['id']
        data = tbl_shopdetails.objects.get(id=id)
        return render(request, 'user/user_add_feedback.html', {'data': data})




def user_add_review(request):
    if request.method == 'POST':
        user_id = request.session['id']
        doctor_id = request.POST.get('doctor_id') 
        msg = request.POST.get('msg')
        uid = tbl_register.objects.get(id=user_id)
        did = tbl_doctor.objects.get(id=doctor_id)
        tbl_review(user_id=uid, doctor_id=did,msg=msg).save()
        return render(request, 'user/user_home.html')
    else:
        id=request.GET['id']
        data = tbl_doctor.objects.get(id=id)
        return render(request, 'user/user_add_review.html', {'data': data})


def user_view_bookings(request):
    id=request.session['id']
    data=tbl_booking.objects.all().filter(user_id=id,doctor_status='completed').select_related('user_id','doctor_id')
    return render(request, 'user/user_view_bookings.html', {'data': data})


def user_cancel_booking(request):
    id=request.GET['id']
    tbl_booking.objects.all().filter(doctor_id=id).update(status='cancel')
    return redirect('user_view_doctor')



def user_view_cancel_booking(request):
    id=request.session['id']
    data=tbl_booking.objects.all().filter(user_id=id,status='canceled').select_related('user_id','doctor_id')
    return render(request, 'user/user_view_cancel_booking.html', {'data': data})



def user_book_again(request):
    id=request.GET['id']
    tbl_booking.objects.all().filter(id=id).update(status='pendings')
    return redirect('user_view_doctor')


from django.utils import timezone

def user_chat(request):    
    if request.method == 'POST':
        user_id = request.session['id']
        doctor_id = request.POST.get('doctor_id') 
        msg = request.POST.get('message')
        uid = tbl_register.objects.get(id=user_id)
        did = tbl_doctor.objects.get(id=doctor_id)
        current_time = timezone.now()  # Get the current time
        tbl_chat(sender=uid, receiver=did, message=msg, utype='user', time=current_time).save()
        data = tbl_doctor.objects.get(id=doctor_id)
        messages = tbl_chat.objects.filter(sender=user_id,receiver=doctor_id).order_by('id')
        return render(request, 'user/chat.html', {'data': data, 'messages': messages})
    else:
        user_id=request.session['id']
        doctor_id = request.GET.get('id')
        data = tbl_doctor.objects.get(id=doctor_id)
        messages = tbl_chat.objects.filter(sender=user_id,receiver=doctor_id).order_by('id')
        return render(request, 'user/chat.html', {'data': data, 'messages': messages})








# ...........................Shop..........................







def shop_home(request):
    return render(request,'shop/shop_home.html')



def shop_profile(request):
    id=request.session['id']
    data=tbl_register.objects.all().filter(id=id)
    return render(request,'shop/shop_profile.html',{'data':data}) 


def shop_editprofile(request,id):
    if request.method == "POST":
        email = request.POST.get('email') 
        phn = request.POST.get('phn')
        name = request.POST.get('name')
        uname = request.POST.get('uname')      
        pswd = request.POST.get('pswd')   
        adrs = request.POST.get('adrs') 
        tbl_register.objects.all().filter(id=id).update(email=email, phn=phn, name=name,uname=uname,pswd=pswd,adrs=adrs)   
        return redirect('shop_profile')  
    else:
        data=tbl_register.objects.all().filter(id=id)
        return render(request, 'shop/shop_editprofile.html',{'data': data})



def shop_add_product(request):
    if request.method=='POST':
        id=request.session['id']
        lname=request.POST.get('lname')
        phn=request.POST.get('phn')
        adrs=request.POST.get('adrs')
        pname=request.POST.get('pname')
        amnt=request.POST.get('amnt')
        qnty=request.POST.get('qnty')
        description=request.POST.get('description')
        files=request.FILES.get('files')
        img=request.FILES.get('img')
        instance=tbl_register.objects.get(id=id)
        tbl_shopdetails(shop_id=instance, lname=lname,phn=phn,pname=pname,amnt=amnt,adrs=adrs,qnty=qnty,files=files,description=description,img=img,status='pending').save()
        return render(request,'shop/shop_home.html')
    else:
        return render(request,'shop/shop_add_product.html')
    


def shop_view_product(request):
    id=request.session['id']
    data=tbl_shopdetails.objects.all().filter(shop_id=id,status='approved')
    print('....',data)
    return render (request,'shop/shop_view_product.html',{'data':data})




def shop_view_file(request):
    id=request.GET.get('shop_id')
    data = get_object_or_404(tbl_shopdetails.objects.filter(shop_id=id).order_by('-id')[:1])
    pdf_file = data.files.read() 
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="data_{id}.pdf"'
    return response 



def shop_edit_product(request,id):
    if request.method == "POST":
        lname = request.POST.get('lname') 
        phn = request.POST.get('phn')
        adrs = request.POST.get('adrs')
        pname = request.POST.get('pname')      
        amnt = request.POST.get('amnt')   
        qnty = request.POST.get('qnty') 
        description = request.POST.get('description') 
        try:
            img_c = request.FILES['img']
            fs = FileSystemStorage()
            image = fs.save(img_c.name, img_c)
        except MultiValueDictKeyError:
            image = tbl_shopdetails.objects.get(id=id).img
        try:
            img_c = request.FILES['files']
            fs = FileSystemStorage()
            file = fs.save(img_c.name, img_c)
        except MultiValueDictKeyError:
            file = tbl_shopdetails.objects.get(id=id).files
       
        tbl_shopdetails.objects.all().filter(id=id).update(lname=lname, phn=phn, adrs=adrs,pname=pname,amnt=amnt,qnty=qnty,description=description,img=image,files=file)   
        return redirect('shop_view_product')  
    else:
        data=tbl_shopdetails.objects.all().filter(id=id)
        return render(request, 'shop/shop_edit_product.html',{'data': data})


def shop_delete_product(request,id):
     tbl_shopdetails.objects.filter(id=id).delete()
     return redirect('shop_view_product')



def shop_view_feedback(request):
    id=request.session['id']
    data=tbl_feedback.objects.all().filter(shop_id=id).select_related('user_id','product_id')
    return render(request,'shop/shop_view_feedback.html',{'data':data}) 




def shop_view_user_orders(request):
    id = request.session.get('id') 
    data = tbl_order.objects.filter(payment_status='paid', product_id__shop_id=id, order_status="pending").select_related('product_id', 'user_id','cart_id')
    return render(request, 'shop/shop_view_user_orders.html', {'data': data})

def dispatch_order(request, order_id):
    order = tbl_order.objects.get(id=order_id)
    order.order_status = 'Dispatched'
    order.save()
    tbl_notifications.objects.create(
            user_id=order.user_id,  # Assuming user is a ForeignKey in tbl_order
            message=f'Your order id ({order.id}) has been dispatched. Thank you for shopping with us!',
            utype='user'  # Add a user-defined type if needed
        )
    return redirect('shop_view_user_orders') 

# ......................doctor...................





def doctor_home(request):
    return render(request,'doctor/doctor_home.html')


def doctor_profile(request):
    id=request.session['id']
    data=tbl_doctor.objects.all().filter(id=id)
    return render(request,'doctor/doctor_profile.html',{'data':data}) 


def doctor_editprofile(request,id):
    if request.method == "POST":
        email = request.POST.get('email') 
        phn = request.POST.get('phn')
        name = request.POST.get('name')
        uname = request.POST.get('uname')      
        pswd = request.POST.get('pswd')   
        adrs = request.POST.get('adrs') 
        tbl_doctor.objects.all().filter(id=id).update(email=email, phn=phn, name=name,uname=uname,pswd=pswd,adrs=adrs)   
        return redirect('doctor_profile')  
    else:
        data=tbl_doctor.objects.all().filter(id=id)
        return render(request, 'doctor/doctor_editprofile.html',{'data': data})
    


def doctor_view_UserMessage(request):
    doctor_id = request.session.get('id')
    var = tbl_message.objects.filter(doctor_id=doctor_id,utype='user').select_related('doctor_id','user_id')
    return render(request, 'doctor/doctor_view_UserMessage.html', {"var": var})


from django.db.models import Count

def doctor_view_chat(request):
    doctor_id = request.session.get('id')
    var = tbl_chat.objects.filter(receiver=doctor_id).values('sender').annotate(message_count=Count('id'))
    senders = tbl_register.objects.filter(id__in=[item['sender'] for item in var])
    chat_data = [{'sender': sender, 'message_count': item['message_count']} for sender, item in zip(senders, var)]
    return render(request, 'doctor/doctor_view_chat.html', {"var": chat_data})



def doctor_add_message(request,id):
    if request.method == 'POST':
        doctor_id = request.session['id']
        user_id = request.POST.get('user_id')
        user_instance = tbl_register.objects.get(id=user_id)
        doctor_instance = tbl_doctor.objects.get(id=doctor_id)
        msg = request.POST.get('msg')
        # img=request.FILES.get('img')
        tbl_message(user_id=user_instance, doctor_id=doctor_instance, msg=msg,utype='doctor').save()
        return render(request, 'doctor/doctor_home.html')
    else:
        data = tbl_register.objects.get(id=id)
        return render(request, 'doctor/doctor_add_message.html', {'data': data})


def doctor_view_alloted_patient(request):
    doctor_id = request.session.get('id')
    data= tbl_booking.objects.all().filter(doctor_id=doctor_id,status='started',doctor_status='pending').select_related('user_id')
    return render(request,'doctor/doctor_view_alloted_patient.html',{'data':data})



def doctor_confirm_patient(request):
    id=request.GET['id']
    tbl_booking.objects.all().filter(id=id).update(doctor_status='confirmed')
    return redirect('doctor_view_alloted_patient')



def doctor_view_confirmed_patient(request):
    doctor_id = request.session.get('id')
    data= tbl_booking.objects.all().filter(doctor_id=doctor_id,status='started',doctor_status='confirmed').select_related('user_id')
    return render(request,'doctor/doctor_view_confirmed_patient.html',{'data':data})


def doctor_complete_checkup(request):
    id=request.GET['id']
    tbl_booking.objects.all().filter(id=id).update(doctor_status='completed')
    return redirect('doctor_view_alloted_patient')


def doctor_view_completed_checkup(request):
    doctor_id = request.session.get('id')
    data= tbl_booking.objects.all().filter(doctor_id=doctor_id,status='started',doctor_status='completed').select_related('user_id')
    return render(request,'doctor/doctor_view_completed_checkup.html',{'data':data})


def doctor_view_products(request):
    data=tbl_shopdetails.objects.all().filter(status='approved').select_related('shop_id')
    return render(request,'doctor/doctor_view_products.html',{'data':data})




def doctor_chat(request):    
    if request.method == 'POST':
        doctor_id = request.session['id']
        user_id = request.POST.get('user_id') 
        msg = request.POST.get('message')
        uid = tbl_register.objects.get(id=user_id)
        did = tbl_doctor.objects.get(id=doctor_id)
        tbl_chat(sender=uid, receiver=did, message=msg, utype='doctor').save()
        data = tbl_register.objects.get(id=user_id)
        messages = tbl_chat.objects.filter(sender=user_id,receiver=doctor_id).order_by('id')
        return render(request, 'doctor/chat.html', {'data': data, 'messages': messages})
    
    else:
        doctor_id=request.session['id']
        user_id = request.GET.get('id')
        data = tbl_register.objects.get(id=user_id)
        messages = tbl_chat.objects.filter(sender=user_id,receiver=doctor_id).order_by('id')
        return render(request, 'doctor/chat.html', {'data': data, 'messages': messages})
    

def doctor_view_notifications(request):
    user_id = request.session.get('id')
    notifications = tbl_doctor_notifications.objects.filter(user_id=user_id , utype="doctor").order_by('-timestamp')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'doctor/doctor_view_notifications.html', context)



# ...........................Admin.............................


def admin_home(request):
    return render(request,'admin/admin_home.html')



def admin_add_doctor(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        category=request.POST.get('category')
        ftime=request.POST.get('ftime')
        ttime=request.POST.get('ttime')
        ftimeval=request.POST.get('ftimeval')
        ttimeval=request.POST.get('ttimeval')
        available_time=''
        available_time=""+ftime+""+""+ftimeval+"" +"-"+ ""+ttime+""+""+ttimeval+""
        tbl_doctor(name=name,uname=uname,email=email,pswd=pswd,adrs=adrs,phn=phn,available_time=available_time,category=category,utype='doctor').save()
        return render(request,'admin/admin_home.html')
    else:
        return render(request,'admin/admin_add_doctor.html')
    


def admin_view_doctor(request):
    data=tbl_doctor.objects.all()
    return render(request,'admin/admin_view_doctor.html',{'data':data}) 



def admin_edit_doctor(request,id):
     if request.method == "POST":
        email = request.POST.get('email') 
        phn = request.POST.get('phn')
        name = request.POST.get('name') 
        adrs = request.POST.get('adrs') 
        category = request.POST.get('category') 
        available_time = request.POST.get('available_time')
        tbl_doctor.objects.all().filter(id=id).update(email=email, phn=phn,category=category, name=name,available_time=available_time,adrs=adrs)   
        return redirect('admin_view_doctor')  
     else:
        data=tbl_doctor.objects.all().filter(id=id)
        return render(request, 'admin/admin_edit_doctor.html',{'data': data})
     

def admin_delete_doctor(request,id):
    tbl_doctor.objects.all().filter(id=id).delete()
    return redirect ('admin_view_doctor')
     


def admin_view_pending_shops(request):
    data=tbl_shopdetails.objects.all().filter(status='pending').select_related('shop_id')
    return render(request,'admin/admin_view_pending_shops.html',{'data':data})


def admin_approve_shops(request):
    id=request.GET['id']
    tbl_shopdetails.objects.all().filter(id=id).update(status='approved')
    return redirect('admin_view_pending_shops')



def admin_reject_shops(request):
    id=request.GET['id']
    tbl_shopdetails.objects.all().filter(id=id).update(status='reject')
    return redirect('admin_view_pending_shops')



def admin_view_approved_shops(request):
    myid = request.session['id']
    data = tbl_shopdetails.objects.all().filter(status='approved').select_related('shop_id')
    return render(request, "admin/admin_view_approved_shops.html", {'data': data})


def admin_view_rejected_shops(request):
    myid = request.session['id']
    data = tbl_shopdetails.objects.all().filter(status='reject').select_related('shop_id')
    return render(request, "admin/admin_view_rejected_shops.html", {'data': data})


def admin_view_bookings(request):
    data= tbl_booking.objects.all().filter(status='pending').select_related('doctor_id','user_id')
    return render(request,'admin/admin_view_bookings.html',{'data':data})


def admin_allocate_doctor(request):
    booking_id = request.GET.get('id')

    if booking_id:
        # Using get_object_or_404 to handle the case where the booking doesn't exist
        booking = get_object_or_404(tbl_booking, id=booking_id)
        # Update the booking status
        booking.status = 'started'
        booking.doctor_status = 'pending'
        booking.save()
        # Get doctor's information
        doctor = get_object_or_404(tbl_doctor, id=booking.doctor_id.id)
        # Create a notification with doctor's name and date of booking
        notification_message = f"Booking Confirmed: Doctor {doctor.name} has been allocated for Booking id {booking_id} on {booking.date}."
        notification = tbl_notifications(user_id=booking.user_id, message=notification_message, timestamp=timezone.now(), utype='user')
        notification.save()
        # Create a notification for doctor with date of booking
        doctor_notification_message = f"Booking Confirmed: You have been allocated for Booking id {booking_id} on {booking.date}."
        doctor_notification = tbl_doctor_notifications(user_id=doctor, message=doctor_notification_message, timestamp=timezone.now(), utype='doctor')
        doctor_notification.save()

    return redirect('admin_view_bookings')



def admin_cancel_booking(request):
    id=request.GET['id']
    tbl_booking.objects.all().filter(id=id).update(status='canceled',doctor_status='pending')
    return redirect('admin_view_bookings')




def admin_view_doctor_status(request):
    data=tbl_booking.objects.all().filter(status='started').select_related('doctor_id','user_id')
    return render(request,'admin/admin_view_doctor_status.html',{'data':data}) 



def admin_view_patient_review(request):
    data=tbl_review.objects.all().select_related('user_id','doctor_id')
    return render(request,'admin/admin_view_patient_review.html',{'data':data}) 




def admin_view_user(request):
    data=tbl_register.objects.all().filter(utype='user')
    return render(request,'admin/admin_view_user.html',{'data':data}) 




def admin_view_patient_feedback(request):
    data=tbl_feedback.objects.all().select_related('user_id','product_id')
    return render(request,'admin/admin_view_patient_feedback.html',{'data':data}) 



def admin_view_user_orders(request):
    data = tbl_order.objects.filter(payment_status='paid').select_related('product_id', 'user_id','cart_id')
    return render(request, 'admin/admin_view_user_orders.html', {'data': data})
