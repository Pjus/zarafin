from django.shortcuts import render
from . import forms

# Create your views here.
def index(request):
    form = forms.SearchForm()
    context = {"form": form}
    return render(request, "login/index.html", context)