from account.models import Account
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth

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
                    messages.info(request,'Not an Admin User')
                    return render(request,'admin_signin.html')
            else:
                messages.info(request,'No User found')
                return render(request,'admin_signin.html')

    else:
        return render(request,'admin_signin.html')


def admin_home(request):
    return render(request, 'admin_home.html')

def active_users(request):
    users = Account.objects.order_by('id').all()
    return render(request,'active_users.html',{'users':users} )
