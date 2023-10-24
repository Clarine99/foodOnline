from vendor.models import Vendors

def get_vendor(request):
    try:
        vendor = Vendors.objects.get(user=request.user)
    except:
        vendor = None
    
    return dict(vendor=vendor)