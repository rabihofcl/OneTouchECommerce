from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from cart.models import BuynowItem, CartItem
from coupon.models import CheckCoupon, Coupon
from product.models import Product
from .forms import OrderForm1, ReviewForm
import datetime
from .models import Order, OrderProduct, Payment, ReviewRating
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import math
import requests
# Create your views here.



	

@never_cache
@login_required(login_url = 'signin')
def payments(request):
    body = json.loads(request.body)

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    # Where USD is the base currency you want to use


    
    #store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    if 'coupon_id' in request.session:
        coupon_id = request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        CheckCoupon.objects.create(user=request.user, coupon= coupon)

        del request.session['coupon_id']
        del request.session['amount_pay']
        del request.session['discount_price']

    # Move the cart items to Order Product Table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer





    # Send order nuber and transaction id back to sendData method via JsonResponse

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }    
    return JsonResponse(data)


@never_cache
@login_required(login_url = 'signin')
def buynow_payments(request):
    body = json.loads(request.body)

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    #store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    if 'coupon_id' in request.session:
        coupon_id = request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        CheckCoupon.objects.create(user=request.user, coupon= coupon)

        del request.session['coupon_id']
        del request.session['amount_pay']
        del request.session['discount_price']

    # Move the cart items to Order Product Table
    buynow_items = BuynowItem.objects.filter(user=request.user)

    for item in buynow_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    BuynowItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer





    # Send order nuber and transaction id back to sendData method via JsonResponse

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }    
    return JsonResponse(data)








@never_cache
@login_required(login_url = 'signin')
def place_order(request, total=0, quantity=0):
    current_user = request.user

    #if the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')


    grand_total = 0
    tax = 0
    discount = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    pre_grand_total = total + tax

    if 'coupon_id' in request.session:
        discount = request.session['discount_price']
        grand_total = request.session['amount_pay']   
    else:
        discount = 0
        grand_total = pre_grand_total
    

    url = 'https://v6.exchangerate-api.com/v6/e71cd6c326f5499dd27514b0/latest/USD'

    # Making our request
    response = requests.get(url)
    data = response.json()
    exchange_rate = data['conversion_rates']['INR']


    price_in_dollar = "%.2f" % (grand_total/exchange_rate)



    if request.method == 'POST':

        form = OrderForm1(request.POST)
        
        if form.is_valid():

            #store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.discount = discount
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #Generating order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")  #20211004
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'price_in_dollar': price_in_dollar,
            }
            return render(request, 'payments.html', context)
    else:
        return redirect('checkout')



@never_cache
@login_required(login_url = 'signin')
def buynow_place_order(request, total=0, quantity=0):
    current_user = request.user

    #if the cart count is less than or equal to 0, then redirect back to shop
    buynow_items = BuynowItem.objects.filter(user=current_user)
    # cart_count = buynow_items.count()
    # if cart_count <= 0:
    #     return redirect('store')


    grand_total = 0
    tax = 0
    discount = 0
    for buynow_item in buynow_items:
        total += (buynow_item.product.price * buynow_item.quantity)
        quantity += buynow_item.quantity
    tax = (2*total)/100
    pre_grand_total = total + tax

    if 'coupon_id' in request.session:
        discount = request.session['discount_price']
        grand_total = request.session['amount_pay']   
    else:
        discount = 0
        grand_total = pre_grand_total
    


    if request.method == 'POST':

        form = OrderForm1(request.POST)
        
        if form.is_valid():

            #store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.discount = discount
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #Generating order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")  #20211004
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': buynow_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'buynow_payments.html', context)
    else:
        return redirect('buy_now')







@never_cache
@login_required(login_url = 'signin')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')






def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                return redirect(url)
            