from django.shortcuts import render,redirect
from django.http import  request, HttpResponse
from .models import User, UserProfile
from .forms import UserForm
from django.contrib import messages
from vendor.forms import VendorForms

# Create your views here.
def registerUser(request):
    if request.method ==  "POST":
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
            # user.save()
            print('user is created', messages)

            messages.error(request, "created succesfully")
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
    if request.method == "POST":
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
            user.role = user.VENDOR
            user.save()
            vendor = v_forms.save(commit=False)
            vendor.user = user 
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Account has been created, please wait for approval')
            context = {
            'form':form, 
            'v_forms':v_forms,
        }
            


    else:
        form = UserForm()
        v_forms = VendorForms()
    context = {
        'form':form, 
        'v_forms':v_forms,
    }
    return render (request, 'accounts/registerVendor.html', context)