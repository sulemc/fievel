from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.http import HttpResponse
from .models import Flagged_Ad


def index(request):
    return HttpResponse("Hello, world. You're at the somewhere index.")

def city(request, ad_location):
    query_city = Flagged_Ad.objects.filter(location=ad_location.title())
    context = {
        'ad_location' : ad_location.title(),
        'query_city' : query_city,
    }
    return render(request, 'city.html', context)