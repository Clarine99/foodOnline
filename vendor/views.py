from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from accounts.forms import UserProfileForm
from .forms import VendorForms
from accounts.models import UserProfile
from .models import Vendors
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendors.objects.get(user=request.user)
    return vendor

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    print('asasasa')
    print(request.POST)
    profile = get_object_or_404(UserProfile, user= request.user)
    vendor = get_object_or_404(Vendors, user= request.user)
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        print("postttttttttttttt")
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForms(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            
            print('updatedd SUKSESSSSSS')
            messages.success(request, 'Settings Updated')
            return redirect ('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForms(instance=vendor)
        print('updatedd kkkkk')
    context = {
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor' : vendor,
    }
    return render (request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder (request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render (request, "vendor/menu_builder.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category (request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    print('this is fooooof itemmm',food_items)
    context = {
        'food_items':food_items,
        'categories':category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            print(str(get_vendor(request)).strip())
            print('FOODDD SLUGGG',category.slug)
            category.save()
            category.slug = slugify(category_name)+"_"+str(category.id)
            category.save()
            messages.success(request, 'Category added succesfully')
            return redirect ('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    context = {
        'form':form,
    }
    return render(request, 'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug =slugify(category_name)
            form.save()
            messages.success(request, 'Category updated succesfully')
            return redirect ('login')
    else:
        form = CategoryForm(instance=category)
        context = {
            'form':form,
            'category':category,
            }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)    
def delete_category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request, 'Succesfully deleted')
    return redirect ('menu_builder')    

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            
            form.save()
            messages.success(request,'Food item added succesfully')
            return redirect ('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm()
        # modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
            'form':form,
            
             }
    return render (request,'vendor/add_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES,instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']

            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item updated succesfully')
            return redirect ('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(get_vendor(request))
        print(form.fields['category'.queryset])
    context = {
            'form':form,
            'food':food,
            }
    return render(request, 'vendor/edit_food.html', context)

def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    print(food)
    messages.success(request, 'Succesfully deleted')
    return redirect ('menu_builder')    
