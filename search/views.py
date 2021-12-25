from django.shortcuts import render
from . import forms


# Create your views here.
def search(request):
    form = forms.SearchForm()
    context = {"form": form}
    return render(request, "search/search.html", context)