from django.shortcuts import render
from . import forms
from .models import *


# Create your views here.
def search(request):
    QGD = QuantGaloreData(Ticker='AAPL')
    data, z_value = QGD.find_z()
    context = {
        'ticker' : request.GET.get('ticker').upper(),
        'data' : data.to_html(),
        'z_value' : round(z_value.values[0], 2),
    }
    return render(request, "search/search_main.html", context=context)