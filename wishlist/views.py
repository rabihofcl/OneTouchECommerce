from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from product.models import Product
from .models import Wishlist

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.




@never_cache
@login_required(login_url = 'signin')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    print(wishlist)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'wishlist.html', context)




@never_cache
@login_required(login_url = 'signin')
def add_wishlist(request):
    id = request.POST['id']

    if Wishlist.objects.filter(user = request.user, product_id=id).exists():
        pass
    else:
        wishlist = Wishlist()
        wishlist.user = request.user
        wishlist.product = Product.objects.get(id=id)
        wishlist.save()

    context = {
        'id': id
    }

    return JsonResponse(context)


@never_cache
@login_required(login_url = 'signin')
def remove_wishlist(request):
    id = request.POST['id']
    Wishlist.objects.get(user=request.user, product_id=id).delete()
    context = {
        'id': id
    }
    return JsonResponse(context)