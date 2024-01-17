from django.shortcuts import render
from django.http import request, HttpResponse
from vendor.models import Vendors

def home(request):
    vendors = Vendors.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        'vendors':vendors,
    }
    return render (request, 'home.html', context)