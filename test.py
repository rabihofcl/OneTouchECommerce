
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
