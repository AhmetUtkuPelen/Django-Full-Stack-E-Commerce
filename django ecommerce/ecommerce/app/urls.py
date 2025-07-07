from django.urls import path
from django.contrib import admin
from .views import*
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import*
from .views import initiate_payment, payment_callback

urlpatterns = [
    path("base/",base,name="base"),
    
    path("",home),
    
    path("category/<slug:val>",CategoryView.as_view(),name="category"),
    
    path('product-detail/<int:id>',ProductDetail.as_view(),name="product-detail"),
    
    path('category-title/<val>',CategoryTitle.as_view(),name="category-title"),
    
    path('about/',about,name="about"),
    
    path('contact/',contact,name="contact"),
    
    path('registration/',CustomerRegistrationView.as_view(),name="customerregistration"),
    
    path('accounts/login',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name="login"),
    
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name="password_reset"),
    
    path('profile/',ProfileView.as_view(),name="profile"),
    
    path('passwordChange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='passwordchangedone'),name="passwordchange"),
    
    path('passwordChangeDone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name="passwordchangedone"),
    # path('logout/',auth_view.LogoutView.as_view(next_page="login"),name="logout"),
    
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name="password_reset"),
    
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name="password_reset_done"),
    
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
    
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name="password_reset_complete"),
    
    path('add-to-cart/',add_to_cart,name="add-to-cart"),
    
    path('cart/',show_cart,name="showcart"),
    
    path('checkout/',Checkout.as_view(),name="checkout"),
    
    path('pluscart/',plus_cart),
    
    path('minuscart/',minus_cart),
    
    path('removecart/',remove_cart),
    
    path('orders/',orders,name="orders"),
    
    path('pluswishlist/',plus_wishlist,name="pluswishlist"),
    
    path('minuswishlist/',minus_wishlist,name="minuswishlist"),
    
    path('search/',search,name="search"),
    
    path('wishlist/',show_wishlist,name="showwishlist"),
    
    path('logout/',user_logout,name="logout"),
    
    path('payment-completed/',paymentCompleted,name="paymentcompleted"),

    path('initiate-payment/', initiate_payment, name='initiate_payment'),
    
    path('payment-callback/', payment_callback, name='payment_callback'),

        
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



# ! ADMIN PAGE TITLE AND HEADER ! #



admin.site.site_header = "AUP TECH"


admin.site.site_title = "AUP TECH"