import json
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
def fetch_packages(request):
    decoded_string = request.body.decode('utf-8')
    data = json.loads(decoded_string)
    payload = data.get('payload')
    destination_name = payload.split('(')[0]
    destination = Destination.objects.get(name = destination_name.strip())
    packages = TourPackage.objects.filter(destination = destination).values("title","destination")
    return JsonResponse({'packages': list(packages)})

@ensure_csrf_cookie
def fetch_tour_details(request):
    print(request.body)
    decorded_string = request.body.decode('utf-8')
    data = json.loads(decorded_string)
    payload = data.get('payload')
    print(payload)
    tours = TourPackage.objects.all().values("title", "category", "destination")
    return JsonResponse({'tours':list(tours)})


def about(request):
    team_members = TeamMember.objects.all().values("first_name", "bio", "role", "photo_url")
    context = {"team_members":list(team_members)}
    return render(request, 'about.html', context)

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
    packages = TourCategory.objects.all().values('name', 'slug')
    context = {
        'packages':packages
    }
    return render(request, 'packages.html', context)

def fetch_custom_packages(request):
    data = json.loads(request.body)
    tour_category = TourCategory.objects.get(slug = data.get('payload'))
    tour_packages = TourPackage.objects.filter(category=tour_category).values('title')
    return JsonResponse({'packages':list(tour_packages)})