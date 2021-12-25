from django.shortcuts import render
from . import forms


# Create your views here.
def search(request):
    print(request.GET.get('ticker'))
    context = {
        'ticker' : request.GET.get('ticker').upper()
    }
    return render(request, "search/search_main.html", context=context)