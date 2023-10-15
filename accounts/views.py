from django.shortcuts import render,redirect
from django.http import  request, HttpResponse
from .models import User, UserProfile
from .forms import UserForm
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, tokens
from django.contrib.auth.decorators import login_required, user_passes_test
from vendor.forms import VendorForms
from .utils import detectUser, send_email_verification
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode

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
            # Send Email Verification
            email_subject = "Activate your account"
            email_template = 'accounts/emails/account_verification_email.html'

            send_email_verification(request, user, email_subject, email_template)
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
            # Send Email Verification
            email_subject = "Activate your account"
            email_template = 'accounts/emails/account_verification_email.html'

            send_email_verification(request, user, email_subject, email_template)
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

def activate(request, uidb64, token):
    # activate the user by setting the is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        print("ini user get managerr", user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and tokens.default_token_generator.check_token(user, token):
        print("activate,", user)
        user.is_active = True
        user.save()
        messages.success(request,"Congrats, Your account is activated!")
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect("myAccount")

    return 


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
    print(user)
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

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            print('ini di forgot password', user)
            email_subject = "Reset Password"
            email_template = 'accounts/emails/reset_password_email.html'
            send_email_verification(request, user, email_subject, email_template)
            # send reset email

            messages.success(request,'Password reset link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request,"Email doesn't exist")
            return redirect ('forgot password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request,uidb64, token):
     # activate the user by setting the is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        print("This in user get manager", user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and tokens.default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request,"Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, 'Link is expired')
        return redirect("myAccount")

    return 
    
def reset_password (request):
    return render (request, "accounts/reset_password.html")