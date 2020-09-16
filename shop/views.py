from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from shop.models import Product, Contact, Orders, OrderItems, UserInfo, Payment
from paytm import Checksum
# OrderItem
from shop.forms import UserForm, ExtendedUserForm
from math import ceil

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import json
from django.views.decorators.csrf import csrf_exempt

MERCHANT_KEY = 'GvYRwo%@Vl2Ml19y'
# MERCHANT_KEY = 'bKMfNxPPf_QdZppa'
# MERCHANT_KEY = 'kbzk1DSbJiV_03p5'

# Create your views here.

def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    cats = sorted(cats)
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)           # n = len(products)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product':products}
    # allProds = [[products, range(1,nSlides), nSlides],[products, range(1,nSlides), nSlides],[products, range(1,nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request,'shop/index.html', params)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def cart(request):
    return render(request, 'shop/cart.html')

def search(request):
    return render(request,'shop/search.html')

def prodview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodView.html',{'product':product[0]})

@login_required
def tracker(request):
    userinfo = UserInfo.objects.get(user=request.user.id)
    orders = Orders.objects.filter(user_id=userinfo)
    return render(request,'shop/tracker.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        extended_user_form = ExtendedUserForm(data=request.POST)
        if user_form.is_valid() and extended_user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['confirm_password']:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            extended = extended_user_form.save(commit=False)
            extended.user = user
            extended.save()
            print("Registered")
            return redirect('User_Login')
        else:
            if user_form.cleaned_data['password'] == user_form.cleaned_data['confirm_password']:
                user_form.add_error('confirm_password', 'Passwords do not match')
            print(user_form.errors, )
    else:
        user_form = UserForm()
        extended_user_form = ExtendedUserForm()
    return render(request, 'shop/registration.html', {'user_form': user_form, 'extended_user_form': extended_user_form})

def user_login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('ShopHome')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        print(username)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print("login")
                # return redirect('ShopHome')
                next = request.POST.get('next','')
                if next == '':
                    next = reverse('ShopHome')
                return HttpResponseRedirect(next)
            else:
                return HttpResponse('Account not active')
        else:
            print("Someone tried to login and failed")
            print(f"Username: {username} and Password: {password}")
            context = {'error': 'Invalid Username or Password'}
    else:
        pass
    return render(request, 'shop/login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ShopHome'))

@login_required
def checkout(request):
    user_id = str(request.user.id)
    # print(request.user.id, type(request.user.id))
    userinfo = UserInfo.objects.get(user=request.user.id)
    if request.method=="POST":
        itemsJSON = request.POST.get('itemsJSON','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')

        products = json.loads(itemsJSON)
        total = 0
        for desc in products.values():
            total = total + (int(desc[0]) * int(desc[3]))
        order = Orders(user_id=userinfo ,no_of_items=len(products),
                       total_price=total, name=name, email=email,
                       address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone)
        order.save()

        for item, desc in products.items():
            order_item = OrderItems(order_id_id=order.order_id,
                                   product_id_id=item[2:],
                                   quantity=desc[0],
                                   price=desc[3])
            order_item.save()

        order_id = str(order.order_id)

        # Request payTm to transfer amount to your payment account
        param_dict = {
            'MID': 'BiDzIl44175596745392', # 'DIY12386817555501617',  'WorldP64425807474247',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
            'MOBILE_NO': '7777777777',
            # 'EMAIL': 'mahajan.anand27@gmail.com',
            'CUST_ID': user_id,
            'ORDER_ID': order_id,
            'TXN_AMOUNT': str(total),
            'MERC_UNQ_REF': user_id
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request,'shop/checkout.html',{'userinfo': userinfo, 'id': id})

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request , this method handle the request

    response_dict = dict(request.POST.items())

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, response_dict['CHECKSUMHASH'])
    if verify:
        user = get_object_or_404(UserInfo, user_id=int(response_dict['MERC_UNQ_REF']))
        if response_dict['STATUS'] == 'TXN_SUCCESS':
            status = 'Success'
        elif response_dict['STATUS'] == 'TXN_FAILURE':
            status = 'Failure'
        else:
            print('status' + response_dict['STATUS'])
            status = 'Pending'
        payment_info = Payment(user_id=user,
                          order_id_id=response_dict['ORDERID'],
                          txn_id=response_dict['TXNID'],
                          bank_txn_id=response_dict['BANKTXNID'],
                          amount=int(float(response_dict['TXNAMOUNT'])),
                          payment_status=status,
                          payment_date_time=response_dict['TXNDATE'] )
        payment_info.save()
        payment_info.change_order_status()
        if response_dict['RESPCODE'] == '01':
            print('Order Successfull' + response_dict['ORDERID'])
        else:
            print('Order not success ' + response_dict['RESPMSG'])
    else:
        print('Someone tries to attack us')
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

@login_required
def cancel_order(request,id):
    pass
