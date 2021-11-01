
from django.db.models.aggregates import Count
from django.http.response import HttpResponse, JsonResponse
from admin_panel.forms import BrandForm
from ads.forms import AdsForm
from brand.models import Brand
from coupon.forms import CouponForm
from coupon.models import Coupon
from orders.forms import OrderForm, OrderProductForm
from product.forms import ProductForm
from product.models import Product
from account.models import Account
from ads.models import Ads
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
import os
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderProduct, Payment
from django.db.models import Q
import datetime
import csv
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

# Create your views here.


def admin_signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_superuser == True:
                auth.login(request, user)
                return redirect('admin_home')
            else:
                messages.info(request, 'Not an Admin User')
                return render(request, 'admin_signin.html')
        else:
            messages.info(request, 'No User found')
            return render(request, 'admin_signin.html')

    else:
        return render(request, 'admin_signin.html')


@login_required(login_url='admin_signin')
def ad_logout(request):
    auth.logout(request)
    return redirect('admin_signin')


@login_required(login_url='admin_signin')
def admin_home(request):
    products = Product.objects.all().count()
    brands = Brand.objects.all().count()
    users = Account.objects.all().count()

    # orders chart data
    labels1 = []
    data1 = []

    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')[:10]
    for order in orders:
        labels1.append(order.order_number)
        data1.append(order.order_total)

    # prodcuts chart data
    labels2 = []
    data2 = []

    products_count = (Product.objects.values(
        'brand__brand_name').annotate(dcount=Count('brand')).order_by())
    for product_count in products_count:
        labels2.append(product_count["brand__brand_name"])
        data2.append(product_count["dcount"])

    payments = Payment.objects.all()
    payment_total = 0
    for payment in payments:
        payment_total += float(payment.amount_paid)


    context = {
        'products': products,
        'brands': brands,
        'users': users,

        'labels': labels1,
        'data': data1,

        'labels2': labels2,
        'data2': data2,

        'payment_total': payment_total,
    }
    return render(request, 'admin_home.html', context)


@login_required(login_url='admin_signin')
def ad_brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'ad_brand_list.html', {'brands': brands})


@login_required(login_url='admin_signin')
def ad_add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save()
            brand.slug = brand.brand_name.lower().replace(" ", "-")
            form.save()
            return redirect('ad_brand_list')
        else:
            return redirect('ad_add_brand')
    else:
        form = BrandForm()

    return render(request, 'ad_add_brand.html', {'form': form})


def ad_delete_brand(request,id):
    Brand.objects.filter(id=id).delete()
    return redirect('ad_brand_list')


@login_required(login_url='admin_signin')
def ad_brand_edit(request, slug):
    brand = Brand.objects.get(slug=slug)

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand = form.save()
            brand.slug = brand.brand_name.lower().replace(" ", "-")
            form.save()
            return redirect('ad_brand_list')

    else:
        form = BrandForm(instance=brand)

    return render(request, 'ad_brand_edit.html', {'brand': brand, 'form': form})


@login_required(login_url='admin_signin')
def ad_product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'ad_product_list.html', {'products': products})


@login_required(login_url='admin_signin')
def ad_add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = product.product_name.lower().replace(" ", "-")
            if product.offer is not None:
                product.price = product.mrp-(product.mrp*product.offer/100)
            else:
                product.price = product.mrp

            product_form.save()
            return redirect('ad_add_product')
        else:
            messages.info(request, 'Product name already exists')
            return redirect('ad_add_product')
    else:
        product_form = ProductForm()

    brands = Brand.objects.all()

    context = {
        'brands': brands,
        'product_form': product_form,
    }
    return render(request, 'ad_add_product.html', context)


@login_required(login_url='admin_signin')
def ad_product_edit(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        product_form = ProductForm(
            request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = product.product_name.lower().replace(" ", "-")
            if product.offer is not None:
                product.price = product.mrp-(product.mrp*product.offer/100)
            else:
                product.price = product.mrp

            product_form.save()
            return redirect('ad_product_list')

    else:
        product_form = ProductForm(instance=product)

    context = {
        'product_form': product_form,
        'product': product,
    }
    return render(request, 'ad_product_edit.html',  context)


@login_required(login_url='admin_signin')
def ad_delete_product(request,id):
    Product.objects.filter(id=id).delete()
    return redirect('ad_product_list')

@login_required(login_url='admin_signin')
def active_users(request):
    users = Account.objects.order_by('id').filter(is_active=True).all()
    return render(request, 'active_users.html', {'users': users})


@login_required(login_url='admin_signin')
def block_user(request,id):
    user = Account.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('active_users')




@login_required(login_url='admin_signin')
def blocked_users(request):
    users = Account.objects.order_by('id').filter(is_active=False).all()
    return render(request, 'blocked_users.html', {'users': users})


@login_required(login_url='admin_signin')
def activate_user(request,id):
    user = Account.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('blocked_users')



@login_required(login_url='admin_signin')
def ad_active_orders(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_at')

    order_detail = OrderProduct.objects.exclude(
        Q(status='Delivered') | Q(status='Cancelled')).order_by('-created_at')

    order_product_form = OrderProductForm()

    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'active_orders': orders,
        'orders': orders,
        'order_detail': order_detail,
        'subtotal': subtotal,
        'order_product_form': order_product_form,
    }
    return render(request, 'ad_active_orders.html', context)


@login_required(login_url='admin_signin')
def change_status(request, id):
    if request.method == 'POST':
        order_product = OrderProduct.objects.get(id=id)
        order_product_form = OrderProductForm(
            request.POST, instance=order_product)

        if order_product_form.is_valid():
            order_product_form.save()
            return redirect('ad_active_orders')
    return redirect('ad_active_orders')


@login_required(login_url='admin_signin')
def order_status_change(request):
    id = request.POST['id']
    status = request.POST['status']
    order_product = OrderProduct.objects.get(id=id)
    order_product.status = status
    order_product.save()
    return JsonResponse({'success': True})

    





@login_required(login_url='admin_signin')
def ad_past_orders(request):

    order_detail = OrderProduct.objects.filter(
        Q(status='Delivered') | Q(status='Cancelled')).order_by('-created_at')
    order_product_form = OrderProductForm()

    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order_product_form': order_product_form,
    }
    return render(request, 'ad_past_orders.html', context)


@login_required(login_url='admin_signin')
def ad_order_edit(request, order_number):
    order_detail = OrderProduct.objects.filter(
        order__order_number=order_number)
    order = Order.objects.get(order_number=order_number)

    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)

        if order_form.is_valid():
            order_form.save()
            return redirect('ad_active_orders')
    else:
        order_form = OrderForm(instance=order)

    context = {
        'order_form': order_form,
        'order': order,
    }

    return render(request, 'ad_order_edit.html', context)


@login_required(login_url='admin_signin')
def ads(request):
    ads_list = Ads.objects.all()


    context = {
        'ads_list': ads_list,
    }
    return render(request, 'ad_ads.html', context)


@login_required(login_url='admin_signin')
def ad_add_ads(request):
    if request.method == 'POST':
        ads_form = AdsForm(request.POST, request.FILES)
        if ads_form.is_valid():
            ads_form.save()

            return redirect('ads')
    else:
        ads_form = AdsForm()

    context = {
        'ads_form': ads_form,
    }
    return render(request, 'ad_add_ads.html', context)


@login_required(login_url='admin_signin')
def delete_ads(request,id):
    Ads.objects.filter(id=id).delete()
    return redirect('ads')

@login_required(login_url='admin_signin')
def report(request):
    if 'date_from' in request.session:
        del request.session['date_from']
        del request.session['date_to']

    if request.method == 'POST':

        if 'date_from' in request.session:
            del request.session['date_from']
            del request.session['date_to']

        date_from = request.POST['datefrom']
        date_to = datetime.datetime.strptime(request.POST['dateto'], "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_to = datetime.datetime.strftime(date_to, "%Y-%m-%d")

        request.session['date_from'] = date_from
        request.session['date_to'] = date_to

        orders = Order.objects.filter(created_at__range=[date_from, date_to], is_ordered=True).order_by('-created_at')
        brands = Brand.objects.all()
        products = Product.objects.all()

        context = {
            'brands': brands,
            'products': products,
            'orders': orders,
        }
        return render(request, 'ad_report.html', context)
    else:
        brands = Brand.objects.all()
        products = Product.objects.all()
        orders = Order.objects.filter(is_ordered=True).order_by('-created_at')

        context = {
            'brands': brands,
            'products': products,
            'orders': orders,
        }
        return render(request, 'ad_report.html', context)


@login_required(login_url='admin_signin')
def brand_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Brands ' + \
        str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['BRAND NAME', 'BRAND ID'])

    brands = Brand.objects.all().order_by('id')

    for brand in brands:
        writer.writerow([brand.brand_name, brand.id])

    return response


@login_required(login_url='admin_signin')
def brand_export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Brands ' + \
        str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Brands')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BRAND NAME', 'BRAND ID']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Brand.objects.all().order_by('id').values_list('brand_name', 'id')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


@login_required(login_url='admin_signin')
def brand_export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename = Brands ' + \
        str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    brands = Brand.objects.all().order_by('id')

    html_string = render_to_string('brand_pdf_output.html', {
                                   'brands': brands, 'total': 0})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required(login_url='admin_signin')
def product_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Products ' + \
        str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['PRODUCT NAME', 'BRAND', 'STOCK', 'PRICE'])

    products = Product.objects.all().order_by('id')

    for product in products:
        writer.writerow([product.product_name, product.brand,
                        product.stock, product.price])

    return response


@login_required(login_url='admin_signin')
def product_export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Products ' + \
        str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['PRODUCT NAME', 'BRAND', 'STOCK', 'PRICE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Product.objects.all().order_by('id').values_list(
        'product_name', 'brand', 'stock', 'price')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


@login_required(login_url='admin_signin')
def product_export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename = Products ' + \
        str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    products = Product.objects.all().order_by('id')

    html_string = render_to_string('product_pdf_output.html', {
                                   'products': products, 'total': 0})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required(login_url='admin_signin')
def order_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Orders ' + \
        str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['ORDER NUMBER', 'FULL NAME', 'PHONE',
                    'EMIAL', 'ORDER TOTAL', 'TAX', 'CREATED AT'])

    if 'date_from' in request.session:
        date_from = request.session['date_from']
        date_to = request.session['date_to']
        orders = Order.objects.filter(created_at__range=[date_from, date_to], is_ordered=True).order_by('-created_at')
    else:
        orders = Order.objects.filter(is_ordered=True).order_by('-created_at')

    for order in orders:
        writer.writerow([order.order_number, order.full_name(
        ), order.phone, order.email, order.order_total, order.tax, order.created_at])

    return response


@login_required(login_url='admin_signin')
def order_export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Orders ' + \
        str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Orders')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ORDER NUMBER', 'FULL NAME', 'PHONE',
               'EMIAL', 'ORDER TOTAL', 'TAX', 'CREATED AT']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    if 'date_from' in request.session:
        date_from = request.session['date_from']
        date_to = request.session['date_to']
        rows = Order.objects.filter(created_at__range=[date_from, date_to], is_ordered=True).order_by('-created_at').values_list(
        'order_number', 'first_name', 'phone', 'email', 'order_total', 'tax', 'created_at')
    else:
        rows = Order.objects.filter(is_ordered=True).order_by('-created_at').values_list(
        'order_number', 'first_name', 'phone', 'email', 'order_total', 'tax', 'created_at')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


@login_required(login_url='admin_signin')
def order_export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename = Orders ' + \
        str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    if 'date_from' in request.session:
        date_from = request.session['date_from']
        date_to = request.session['date_to']
        orders = Order.objects.filter(created_at__range=[date_from, date_to], is_ordered=True).order_by('-created_at')
    else:
        orders = Order.objects.filter(is_ordered=True).order_by('-created_at')

    html_string = render_to_string('order_pdf_output.html', {
                                   'orders': orders, 'total': 0})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required(login_url='admin_signin')
def coupon(request):

    coupon_form = CouponForm()
    coupons = Coupon.objects.all()

    context = {
        'coupon_form': coupon_form,
        'coupons': coupons,
    }
    return render(request, 'ad_coupon.html', context)


@login_required(login_url='admin_signin')
def add_coupon(request):
    coupon_form = CouponForm(request.POST)
    if coupon_form.is_valid():
        coupon = coupon_form.save(commit=False)
        coupon.status = True
        coupon_form.save()
    return JsonResponse({'success': True})


def ad_delete_coupon(request):
    id = request.POST['id']
    print(id)
    Coupon.objects.filter(id=id).delete()
    return JsonResponse({'success': True})

