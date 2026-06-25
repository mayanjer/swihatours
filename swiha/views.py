from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def home(request):
    destinations = Destination.objects.all()
    tour_types = TourCategory.objects.all()

    context = {
        'destinations':destinations,
        'tour_types':tour_types
    }
    return render(request, 'index.html', context)

def fetch_destinations(request):
    
    return redirect(home)


def about(request):
    return render(request, 'about.html')

def booking(request):
    return render(request, 'booking.html')

def blog(request):
    return render(request, 'blog.html')

def booking(request):
    return render(request, 'booking.html')

def contact(request):
    return render(request, 'contact.html')

def destination(request):
    return render(request, 'destinations.html')

def gallery(request):
    return render(request, 'gallery.html')

def packages(request):
    return render(request, 'packages.html')