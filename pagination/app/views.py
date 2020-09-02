import math
from urllib.parse import urlencode

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .settings import BUS_STATION_CSV
import csv

with open (BUS_STATION_CSV, newline='', encoding='cp1251') as csvfile:
    DATA = [bus for bus in csv.DictReader(csvfile)]

def get_page_url(path, **kwargs):
    return path + '?' + urlencode(kwargs)


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    paginator = Paginator(DATA, 10)
    current_page = request.GET.get('page', 1)
    page_obj = paginator.get_page(current_page)
    next_page_param, prev_page_param = None, None
    if page_obj.has_next():
        next_page_param = get_page_url(reverse(bus_stations), page=int(page_obj.next_page_number()))
    if page_obj.has_previous():
        prev_page_param = get_page_url(reverse(bus_stations), page=int(page_obj.previous_page_number()))
    return render(request, 'index.html', context={
        'bus_stations': page_obj,
        'current_page': current_page,
        'prev_page_url': prev_page_param,
        'next_page_url': next_page_param,
    })

