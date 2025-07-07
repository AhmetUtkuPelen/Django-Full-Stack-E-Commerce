from django.shortcuts import render,redirect
from django.views import View
from .models import*
from django.db.models import Count
from .forms import*
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
import os
import iyzipay
from iyzipay import CheckoutFormInitialize, CheckoutForm
import uuid
import json
from decimal import Decimal
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.



# IYZICO API KEYS
IYZICO_API_KEY = os.environ.get('IYZICO_API_KEY')
IYZICO_SECURITY_KEY = os.environ.get('IYZICO_SECURITY_KEY')
IYZICO_CEP_POS_API_KEY = os.environ.get('IYZICO_CEP_POS_API_KEY')
IYZICO_CEP_SECURITY_KEY = os.environ.get('IYZICO_CEP_SECURITY_KEY')
IYZICO_BASE_URL = 'sandbox-api.iyzipay.com'
# IYZICO API KEYS


options = {
    'api_key': IYZICO_API_KEY,
    'secret_key': IYZICO_SECURITY_KEY,
    'base_url': IYZICO_BASE_URL
}



def base(request):
    return render(request,'app/base.html')




def home(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/home.html',locals())




def about(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())





def contact(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())





class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())




    
class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product =Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,'app/category.html',locals())





class ProductDetail(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        totalitem = 0
        wishitem = 0
        wishlist = False

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # Check if this specific product is in user's wishlist
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user)).exists()

        return render(request,'app/productdetail.html',locals())


    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratz! You Registered Successfully! ")
            return redirect('login')
        else:
            messages.warning(request,"Invalid Data! ")
        return render(request,'app/customerregistration.html',locals())




@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    
    def post(self, request):  # This was incorrectly named 'get'
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            # Create customer instance but don't save yet
            customer = form.save(commit=False)
            # Assign the current user
            customer.user = request.user
            # Save the customer
            customer.save()
            messages.success(request, "Congratulations! Profile Created Successfully!")
            return redirect('checkout')  # Redirect to checkout after successful profile creation
        else:
            messages.warning(request, "Invalid Data")
        return render(request, 'app/profile.html', locals())
    
    
    

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product =Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')






def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity*p.product.discount_price
        amount = amount + value
        totalamount= amount +20
        totalitem = 0
        wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())





def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user =request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=amount + value
            totalamount= amount + 20
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
    




def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
            totalamount = amount + 20
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount,
            }
            return JsonResponse(data)






def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
            totalamount = amount + 20
            data={
                'amount':amount,
                'totalamount':totalamount,
            }
            return JsonResponse(data)
        





class Checkout(View):
    def get(self, request):
        user = request.user
        
        # Check if user is authenticated
        if not user.is_authenticated:
            messages.error(request, 'Please login to proceed with checkout.')
            return redirect('login')
        
        # Get user addresses
        add = Customer.objects.filter(user=user)
        
        # Check if user has any addresses
        if not add.exists():
            messages.warning(request, 'Please add a delivery address before checkout.')
            return redirect('profile')  # Redirect to profile page to add address
        
        # Get cart items
        cart_items = Cart.objects.filter(user=user)
        
        # Check if cart is empty
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty. Please add items to cart.')
            return redirect('show_cart')
        
        # Calculate totals
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 20
        
        return render(request, 'app/checkout.html', locals())
    




def orders(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlace.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())





def show_wishlist(request):
    user =request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,"app/wishlist.html",locals())





@csrf_exempt
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET.get('prod_id')
            if not prod_id:
                return JsonResponse({'message': 'Product ID is required!'})

            product = Product.objects.get(id=prod_id)
            user = request.user

            # Check if product is already in wishlist
            if not Wishlist.objects.filter(user=user, product=product).exists():
                Wishlist.objects.create(user=user, product=product)
                data = {
                    'message': 'You Added This Product To Your Wishlist Successfully!',
                }
            else:
                data = {
                    'message': 'This Product Is Already In Your Wishlist!',
                }
            return JsonResponse(data)
        except Product.DoesNotExist:
            data = {
                'message': 'Product not found!',
            }
            return JsonResponse(data)
        except Exception as e:
            # Add more detailed error message for debugging
            data = {
                'message': f'An error occurred while adding to wishlist: {str(e)}',
            }
            return JsonResponse(data)
    else:
        return JsonResponse({'message': 'Invalid request method!'})
    




@csrf_exempt
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET.get('prod_id')
            if not prod_id:
                return JsonResponse({'message': 'Product ID is required!'})

            product = Product.objects.get(id=prod_id)
            user = request.user

            # Check if product exists in wishlist before removing
            wishlist_item = Wishlist.objects.filter(user=user, product=product)
            if wishlist_item.exists():
                wishlist_item.delete()
                data = {
                    'message': 'You Removed This Product From Your Wishlist Successfully!',
                }
            else:
                data = {
                    'message': 'This Product Is Not In Your Wishlist!',
                }
            return JsonResponse(data)
        except Product.DoesNotExist:
            data = {
                'message': 'Product not found!',
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                'message': f'An error occurred while removing from wishlist: {str(e)}',
            }
            return JsonResponse(data)
    else:
        return JsonResponse({'message': 'Invalid request method!'})




def search(request):
    query = request.GET['search']
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title_icontains=query))
    return render(request,'app/search.html',locals())




def user_logout(request):
    logout(request)
    return redirect('home')




def paymentCompleted(request):
    return render(request,'app/paymentcompleted.html')





# Iyzico Payment Integration

def initiate_payment(request):
    """Initialize Iyzico payment process"""
    if request.method == 'POST':
        user = request.user
        custid = request.POST.get('custid')
        
        # Check if customer ID is provided
        if not custid:
            messages.error(request, 'Please select a delivery address before proceeding to payment.')
            return redirect('checkout')
        
        try:
            # Get customer and cart details
            customer = Customer.objects.get(id=custid)
        except Customer.DoesNotExist:
            messages.error(request, 'Selected address not found. Please select a valid address.')
            return redirect('checkout')
        
        # Check if user has items in cart
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty. Please add items to cart before checkout.')
            return redirect('show_cart')
        
        # Calculate total amount
        amount = 0
        for item in cart_items:
            amount += item.quantity * item.product.discount_price
        total_amount = amount + 20  # Adding shipping cost
        
        # Create payment record
        payment = Payment.objects.create(
            user=user,
            amount=total_amount,
            pay_order_id=str(uuid.uuid4()),
        )
        
        # Prepare Iyzico payment request
        request_data = {
            'locale': 'tr',
            'conversationId': str(payment.id),
            'price': str(total_amount),
            'paidPrice': str(total_amount),
            'currency': 'TRY',
            'installment': '1',
            'basketId': f'B{payment.id}',
            'paymentChannel': 'WEB',
            'paymentGroup': 'PRODUCT',
            'callbackUrl': request.build_absolute_uri(reverse('payment_callback')),
            'enabledInstallments': ['2', '3', '6', '9']
        }
        
        # Buyer information
        buyer = {
            'id': str(user.id),
            'name': customer.name.split()[0] if customer.name else 'Customer',
            'surname': customer.name.split()[-1] if len(customer.name.split()) > 1 else 'User',
            'gsmNumber': str(customer.mobile),
            'email': user.email or 'customer@example.com',
            'identityNumber': '74300864791',  # Dummy for sandbox
            'lastLoginDate': '2015-10-05 12:43:35',
            'registrationDate': '2013-04-21 15:12:09',
            'registrationAddress': f'{customer.locality}, {customer.city}',
            'ip': get_client_ip(request),
            'city': customer.city,
            'country': 'Turkey',
            'zipCode': str(customer.zipcode)
        }
        
        # Shipping and billing address
        shipping_address = {
            'contactName': customer.name,
            'city': customer.city,
            'country': 'Turkey',
            'address': f'{customer.locality}, {customer.city}, {customer.state}',
            'zipCode': str(customer.zipcode)
        }
        
        billing_address = shipping_address.copy()
        
        # Basket items
        basket_items = []
        for item in cart_items:
            basket_item = {
                'id': str(item.product.id),
                'name': item.product.title,
                'category1': item.product.category,
                'itemType': 'PHYSICAL',
                'price': str(item.quantity * item.product.discount_price)
            }
            basket_items.append(basket_item)

        # Add shipping as basket item
        shipping_item = {
            'id': 'SHIPPING',
            'name': 'Shipping Cost',
            'category1': 'Shipping',
            'itemType': 'PHYSICAL',
            'price': '20'
        }
        basket_items.append(shipping_item)
        
        # Complete request data
        request_data.update({
            'buyer': buyer,
            'shippingAddress': shipping_address,
            'billingAddress': billing_address,
            'basketItems': basket_items
        })
        
        try:
            # Initialize payment with Iyzico
            checkout_form_initialize = CheckoutFormInitialize()
            result = checkout_form_initialize.create(request_data, options)

            # Get the response content
            if hasattr(result, 'read'):
                # If it's an HTTPResponse object
                response_content = result.read().decode('utf-8')
            elif hasattr(result, 'content'):
                # If it's a requests Response object
                response_content = result.content.decode('utf-8')
            else:
                # If it's already a string
                response_content = str(result)

            # Parse the JSON response
            import json
            response_data = json.loads(response_content)

            if response_data.get('status') == 'success':
                # Store payment token for later verification
                payment.pay_payment_id = response_data.get('token')
                payment.save()

                # Store payment ID in session for callback
                request.session['payment_id'] = payment.id

                # Get the checkout form content
                checkout_form_content = response_data.get('checkoutFormContent')

                # Create a simple HTML page that will redirect to Iyzico
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Redirecting to Payment...</title>
                </head>
                <body>
                    <div style="text-align: center; margin-top: 50px;">
                        <h3>Redirecting to secure payment page...</h3>
                        <p>Please wait while we redirect you to the payment form.</p>
                    </div>
                    {checkout_form_content}
                </body>
                </html>
                """

                from django.http import HttpResponse
                return HttpResponse(html_content)
            else:
                error_message = response_data.get('errorMessage', 'Unknown error occurred')
                messages.error(request, f'Payment initialization failed: {error_message}')
                return redirect('checkout')
        except Exception as e:
            messages.error(request, f'Payment system error: {str(e)}')
            return redirect('checkout')
    
    return redirect('checkout')


def payment_callback(request):
    """Handle Iyzico payment callback"""
    token = request.POST.get('token')
    payment_id = request.session.get('payment_id')
    
    if not token or not payment_id:
        messages.error(request, 'Invalid payment callback')
        return redirect('checkout')
    
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # Retrieve checkout form result
        request_data = {
            'locale': 'tr',
            'conversationId': str(payment.id),
            'token': token
        }

        checkout_form_result = CheckoutForm()
        result = checkout_form_result.retrieve(request_data, options)

        # Get the response content
        if hasattr(result, 'read'):
            # If it's an HTTPResponse object
            response_content = result.read().decode('utf-8')
        elif hasattr(result, 'content'):
            # If it's a requests Response object
            response_content = result.content.decode('utf-8')
        else:
            # If it's already a string
            response_content = str(result)

        # Parse the JSON response
        response_data = json.loads(response_content)

        if response_data.get('status') == 'success':
            # Payment successful
            payment.paid = True
            payment.pay_payment_status = 'SUCCESS'
            payment.pay_payment_id = response_data.get('paymentId')
            payment.save()

            # Create order records
            user = request.user
            customer = Customer.objects.get(user=user)
            cart_items = Cart.objects.filter(user=user)

            for item in cart_items:
                OrderPlace.objects.create(
                    user=user,
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment,
                    status='Pending'
                )

            # Clear cart
            cart_items.delete()

            # Clear session
            if 'payment_id' in request.session:
                del request.session['payment_id']

            messages.success(request, 'Payment completed successfully!')
            return redirect('paymentcompleted')
        else:
            # Payment failed
            payment.pay_payment_status = 'FAILED'
            payment.save()
            error_message = response_data.get('errorMessage', 'Unknown error occurred')
            messages.error(request, f'Payment failed: {error_message}')
            return redirect('checkout')
            
    except Payment.DoesNotExist:
        messages.error(request, 'Payment record not found')
        return redirect('checkout')
    except Exception as e:
        messages.error(request, f'Payment processing error: {str(e)}')
        return redirect('checkout')


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip