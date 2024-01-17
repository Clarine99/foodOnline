from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse, HttpRequest
from vendor.models import Vendors
from django.shortcuts import get_object_or_404
from vendor.models import Vendors
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from marketplace.models import Cart
from .context_processors import get_cart_counter, get_cart_amount
from django.contrib.auth.decorators import login_required
# Create your views here.

def marketplace (request):
    vendors = Vendors.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render (request, 'marketplace/listings.html',context)

def vendor_detail (request, vendor_slug):
    vendor = get_object_or_404(Vendors, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems', queryset=FoodItem.objects.filter(is_available=True))
        )
    if request.user.is_authenticated :
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render (request, 'marketplace/vendor_detail.html', context )

def add_to_cart(request, food_id=None):

    if request.user.is_authenticated:
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                    
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the cart has already added the food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase cart quantity
                    chkCart.quantity += 1 
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increase the cart quantity', 'cart_counter':get_cart_counter(request),'qty':chkCart.quantity, 'cart_amount':get_cart_amount(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added the food to the cart', 'cart_counter':get_cart_counter(request),'qty':chkCart.quantity, 'cart_amount':get_cart_amount(request)})


            except:
                return JsonResponse({'status': 'Failed', 'message':'Food doesnt exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid Request'})
    else:
        return JsonResponse({'status': 'Failed', 'message':'Please login to continue'})
               
           
def decrease_cart (request, food_id=None):
    if request.user.is_authenticated:
       
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            try:

                fooditem = FoodItem.objects.get(id=food_id)
                try :
                    chckCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chckCart.quantity > 0:
                        chckCart.quantity -= 1
                        chckCart.save()
                        return JsonResponse({'status':'Success', 'message':'decrease the cart quantity', 'cart_counter': get_cart_counter(request), 'qty':chckCart.quantity,'cart_amount':get_cart_amount(request)})
                    else :
                        chckCart.delete()
                        chckCart.quantity = 0
                        return JsonResponse({'status':'Failed', 'message':'decrease the cart quantity', 'cart_counter': get_cart_counter(request),'qty':chckCart.quantity,'cart_amount':get_cart_amount(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message': 'You don\'t have this item in your cart', 'qty':chckCart.quantity})
            except:  
                return JsonResponse({'status': 'Failed', 'message':'Food doesnt exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Please login to continue'})

@login_required(login_url='login')      
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    subtotal = 0
    tax = 0
    grand_total = 0

    if request.user.is_authenticated:
        for item in cart_items :
            foodItem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (foodItem.price * item.quantity)
        grand_total = subtotal + tax
        print(f"subtotal: {subtotal}\nGrand TOtal:{grand_total}")
    context = {
        'cart_items':cart_items,
        'subtotal':subtotal,
        'grand_total':grand_total,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated :
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Sucess', 'message':'cart item has been deleted','cart_counter': get_cart_counter(request),'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message':'Cart item doesnt exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid Request'})
        
