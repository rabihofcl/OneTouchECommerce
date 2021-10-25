


from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from account.models import Address
from admin_panel.views import coupon
from orders.models import Order
from product.models import Product
from cart.models import Cart, CartItem
from coupon.models import CheckCoupon, Coupon

from django.contrib.auth.decorators import login_required
import math
from django.views.decorators.cache import never_cache

# Create your views here.



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



@never_cache
def add_cart(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)  # get the product

    if request.user.is_authenticated:
        try:
            # get the cart using the cart id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            if cart_item.quantity > cart_item.product.stock-1:
                print('out of stock')
                messages.info(request, 'Product Out of Stock')
                return redirect('cart')
            else:
                cart_item.quantity += 1
                cart_item.save()


        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
            )
            cart_item.save()

    else:
        try:
            # get the cart using the cart id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity > cart_item.product.stock-1:
                print('out of stock')
                messages.info(request, 'Product Out of Stock')
                return redirect('cart')
            else:
                cart_item.quantity += 1
                cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
    return redirect(url)


@never_cache
def remove_cart(request):
    product_id = request.POST['id']
    print(id)
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return JsonResponse({'success': True})


@never_cache
def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')


@never_cache
def remove_item(request):
    product_id = request.POST['id']
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return JsonResponse({'success': True})
    

@never_cache
def add_item(request):
    product_id = request.POST['id']
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        try:
            # get the cart using the cart id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            if cart_item.quantity > cart_item.product.stock-1:
                print('out of stock')
                messages.info(request, 'Product Out of Stock')
                return JsonResponse({'success': True})
            else:
                cart_item.quantity += 1
                cart_item.save()


        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
            )
            cart_item.save()

    else:
        try:
            # get the cart using the cart id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity > cart_item.product.stock-1:
                messages.info(request, 'Product Out of Stock')
                return JsonResponse({'success': True})
            else:
                cart_item.quantity += 1
                cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
    return JsonResponse({'success': True})



@never_cache
@login_required(login_url = 'signin')
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)




@never_cache
@login_required(login_url = 'signin')
def checkout(request, total=0, quantity=0, cart_items=None):


    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        del request.session['amount_pay']
        del request.session['discount_price']


    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignore

    addresses = Address.objects.filter(user=request.user)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'addresses': addresses,
    }
    return render(request, 'checkout.html', context)


@never_cache
@login_required(login_url = 'signin')
def Check_coupon(request):
    flag = 0
    discount_price = 0
    amount_pay = 0
    coupon_code = request.POST.get('coupon_code')
    grand_total = float(request.POST.get('grand_total'))

    if Coupon.objects.filter(coupon_code=coupon_code).exists():
        coupon = Coupon.objects.get(coupon_code=coupon_code)
        if coupon.status == True:
            flag = 1
            if not CheckCoupon.objects.filter(user=request.user, coupon = coupon):
                
                discount_price = math.ceil(grand_total*int(coupon.discount)/100)
                amount_pay = grand_total-discount_price
                flag = 2
                request.session['amount_pay'] = amount_pay
                request.session['coupon_id'] = coupon.id
                request.session['discount_price'] = discount_price


    context = {
        'amount_pay': amount_pay,
        'flag': flag,
        'discount_price': discount_price,
    }

    return JsonResponse(context)


@never_cache
@login_required(login_url = 'signin')
def buy_now(request,id,tax=0, total=0, quantity=0, cart_items=None):
    CartItem.objects.all().delete()
    
    product = Product.objects.get(id=id)
    try:
        # get the cart using the cart id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, user=request.user)
        if cart_item.quantity > cart_item.product.stock-1:
            messages.info(request, 'Product Out of Stock')
            return redirect('cart')
        else:
            cart_item.quantity += 1
            cart_item.save()


    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=request.user,
        )
        cart_item.save()


    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignore

    addresses = Address.objects.filter(user=request.user)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'addresses': addresses,
    }
    return render(request, 'buy_now_checkout.html', context)
