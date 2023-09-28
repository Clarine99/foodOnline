from django.shortcuts import render,redirect
from django.http import  request, HttpResponse
from .models import User, UserProfile
from .forms import UserForm
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from vendor.forms import VendorForms
from .utils import detectUser
from django.core.exceptions import PermissionDenied

# Create your views here.

# Restrict the vendor from  accessing vendor page
def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
# Restrict the vendor from  accessing vendor page
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are logged in")
        return redirect ('myAccount')
    elif request.method ==  "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.role = user.CUSTOMER
            # user.set_password(password)
            # print('validate formmmmm')
            # user.save()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            print('user is created', messages)

            messages.success(request, "created succesfully")
            return redirect ('registerUser')
        else:
            print(form.errors)

    else:
        form = UserForm()
    context = {
        'form':form,
        }
    return render (request, 'accounts/registeruser.html', context)
        

def registerVendor (request):
    if request.user.is_authenticated:
        messages.warning(request, "You are logged in")
        return redirect ('myAccount')
    elif request.method == "POST":
    #     form = UserForm(request.POST)
        form = UserForm(request.POST)
        v_forms = VendorForms(request.POST, request.FILES)
        if form.is_valid() and v_forms.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_forms.save(commit=False)
            vendor.user = user 
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Account has been created, please wait for approval')
            return redirect ('login')
          
    else:
        form = UserForm()
        v_forms = VendorForms()
    
    context = {
        'form':form, 
        'v_forms':v_forms,
    }
    return render (request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        print(request)
        messages.warning(request, "You are logged in")
        return redirect ('myAccount')

    elif request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

        user = auth.authenticate(email=email, password=password)
        print(user)
       
        if user is not None:
            auth.login(request, user)
            messages.success(request,"You have successfully login")
            return redirect ('myAccount' )
        else:
            messages.error(request, 'invalid credential')
            return redirect ('login')
   
    return render (request,'accounts/login.html')

    form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)
def logout(request):
    auth.logout(request)
    messages.info(request, "You are Loged Out")
    return redirect ('login')
@login_required(login_url='login')
def myAccount (request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')