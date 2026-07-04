from django.shortcuts import render, redirect
from django.db.models import Count
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import *

# Create your views here.
def home(request):
    destinations = Destination.objects.all()[:5]
    best_tour_packages = TourPackage.objects.all()[:3]
    available_tours = TourPackage.objects.values('destination').annotate(total=Count('id'))
    context = {
        'destinations':destinations,
        'best_tour_packages':list(best_tour_packages),
        'available_tours': available_tours
    }
    return render(request, 'index.html', context)

# this view belongs to the fetch API on index.html
@ensure_csrf_cookie
def fetch_destinations(request):
    destinations = Destination.objects.all().values("name")
    return JsonResponse({'destinations':list(destinations)})

@ensure_csrf_cookie
def fetch_tour_details(request):
    tours = TourPackage.objects.all().values("title")
    return JsonResponse({'tours':list(tours)})


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