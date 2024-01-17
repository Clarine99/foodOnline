from .models import Cart
from menu.models import FoodItem

def get_cart_counter (request):
    cart_count = 0
    
    if request.user.is_authenticated :
        print('cart AUthenticatedddd')
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart_item in cart_items:
                if cart_item:
                    cart_count += cart_item.quantity
                    
                else :
                    print('cart item 000000000000')
                    cart_count = 0
                    
        except:
            cart_count = 0
            
        return dict(cart_count=cart_count)
    else:
        return dict(cart_count=cart_count)
        
def get_cart_amount(request):
    subtotal = 0
    tax = 0
    grand_total = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items :
            foodItem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (foodItem.price * item.quantity)
        
        grand_total = subtotal + tax
        print(f"subtotal : {subtotal} \nGrandtotal : {grand_total}")
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)