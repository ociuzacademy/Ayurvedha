from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
   
   path('',views.index,name="index"),
   path('user_reg/',views.user_reg,name="user_reg"),
   path('shop_reg/',views.shop_reg,name="shop_reg"),
   path('login/',views.login,name="login"),
   path('logout/',views.logout,name="logout"),




   path('user_home/',views.user_home,name="user_home"),
   path('user_profile/',views.user_profile,name="user_profile"),
   path('user_editprofile/<int:id>/',views.user_editprofile,name="user_editprofile"),
   path('user_view_doctor/',views.user_view_doctor,name="user_view_doctor"),
   path('user_add_message/<int:id>/',views.user_add_message,name="user_add_message"),
   path('user_view_DoctorMessage/',views.user_view_DoctorMessage,name="user_view_DoctorMessage"),
   path('user_view_shops/',views.user_view_shops,name="user_view_shops"),
   path('user_view_product/',views.user_view_product,name="user_view_product"),
   path('user_view_product_details/',views.user_view_product_details,name="user_view_product_details"),
   path('add_to_cart/',views.add_to_cart,name="add_to_cart"),
   path('user_cartpage/',views.user_cartpage,name="user_cartpage"),
   path('cart_product_payment/',views.cart_product_payment,name="cart_product_payment"),
   path('delete_cart/',views.delete_cart,name="delete_cart"),
   path('user_payment/',views.user_payment,name="user_payment"),
   path('user_orders/',views.user_orders,name="user_orders"),
   path('user_booking_doctor/',views.user_booking_doctor,name="user_booking_doctor"),
   path('user_view_doctor_confirmation/',views.user_view_doctor_confirmation,name="user_view_doctor_confirmation"),
   path('user_add_feedback/',views.user_add_feedback,name="user_add_feedback"),
   path('user_add_review/',views.user_add_review,name="user_add_review"),
   path('user_view_bookings/',views.user_view_bookings,name="user_view_bookings"),
   path('user_cancel_booking/',views.user_cancel_booking,name="user_cancel_booking"),
   path('user_view_cancel_booking/',views.user_view_cancel_booking,name="user_view_cancel_booking"),
   path('user_book_again/',views.user_book_again,name="user_book_again"),
   path('user_chat/',views.user_chat),
   path('user_view_notifications/', views.user_view_notifications, name='user_view_notifications'),
   
  

   








   path('shop_home/',views.shop_home,name="shop_home"),
   path('shop_profile/',views.shop_profile,name="shop_profile"),
   path('shop_editprofile/<int:id>/',views.shop_editprofile,name="shop_editprofile"), 
   path('shop_add_product/',views.shop_add_product,name="shop_add_product"),
   path('shop_view_product/',views.shop_view_product,name="shop_view_product"),
   path('shop_view_file/',views.shop_view_file,name="shop_view_file"),
   path('shop_edit_product/<int:id>/',views.shop_edit_product,name="shop_edit_product"),
   path('shop_delete_product/<int:id>/',views.shop_delete_product,name="shop_delete_product"),
   path('shop_view_feedback/',views.shop_view_feedback,name="shop_view_feedback"),
   path('shop_view_user_orders/',views.shop_view_user_orders,name="shop_view_user_orders"),
   path('dispatch_order/<int:order_id>/',views.dispatch_order,name="dispatch_order"),
   path('shop_view_notifications/', views.shop_view_notifications, name='shop_view_notifications'),

 
 



   path('doctor_home/',views.doctor_home,name="doctor_home"),
   path('doctor_profile/',views.doctor_profile,name="doctor_profile"),
   path('doctor_editprofile/<int:id>/',views.doctor_editprofile,name="doctor_editprofile"),
   path('doctor_view_UserMessage/',views.doctor_view_UserMessage,name="doctor_view_UserMessage"),
   path('doctor_add_message/<int:id>/',views.doctor_add_message,name="doctor_add_message"),
   path('doctor_view_alloted_patient',views.doctor_view_alloted_patient,name="doctor_view_alloted_patient"),
   path('doctor_confirm_patient/',views.doctor_confirm_patient,name="doctor_confirm_patient"),
   path('doctor_view_confirmed_patient/',views.doctor_view_confirmed_patient,name="doctor_view_confirmed_patient"),
   path('doctor_complete_checkup/',views.doctor_complete_checkup,name="doctor_complete_checkup"),
   path('doctor_view_completed_checkup/',views.doctor_view_completed_checkup,name="doctor_view_completed_checkup"),
   path('doctor_view_products/',views.doctor_view_products,name="doctor_view_products"),
   path('doctor_chat/',views.doctor_chat),
   path('doctor_view_chat/',views.doctor_view_chat),
   path('doctor_view_notifications/', views.doctor_view_notifications, name='doctor_view_notifications'),





   path('admin_home/',views.admin_home,name="admin_home"),
   path('admin_add_doctor/',views.admin_add_doctor,name="admin_add_doctor"),
   path('admin_view_doctor/',views.admin_view_doctor,name="admin_view_doctor"),
   path('admin_edit_doctor/<int:id>/',views.admin_edit_doctor,name="admin_edit_doctor"),
   path('admin_delete_doctor/<int:id>/',views.admin_delete_doctor,name="admin_delete_doctor"),
   path('admin_view_pending_shops/',views.admin_view_pending_shops,name="admin_view_pending_shops"),
   path('admin_approve_shops/',views.admin_approve_shops,name="admin_approve_shops"),
   path('admin_reject_shops/',views.admin_reject_shops,name="admin_reject_shops"),
   path('admin_view_approved_shops/',views.admin_view_approved_shops,name="admin_view_approved_shops"),
   path('admin_view_rejected_shops/',views.admin_view_rejected_shops,name="admin_view_rejected_shops"),
   path('admin_view_bookings/',views.admin_view_bookings,name="admin_view_bookings"),
   path('admin_allocate_doctor/',views.admin_allocate_doctor,name="admin_allocate_doctor"),
   path('admin_view_doctor_status/',views.admin_view_doctor_status,name="admin_view_doctor_status"),
   path('admin_view_patient_review/',views.admin_view_patient_review,name="admin_view_patient_review"),
   path('admin_view_user/',views.admin_view_user,name="admin_view_user"),
   path('admin_view_patient_feedback/',views.admin_view_patient_feedback,name="admin_view_patient_feedback"),
   path('admin_view_user_orders/',views.admin_view_user_orders,name="admin_view_user_orders"),
   path('admin_cancel_booking/',views.admin_cancel_booking,name="admin_cancel_booking"),







   



]