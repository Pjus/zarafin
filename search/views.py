from django.shortcuts import render
from . import forms
from .models import *
import sqlite3

# Create your views here.
def search(request):
    ticker = request.GET.get('ticker').upper()
    QGD = QuantGaloreData(Ticker=ticker)
    data, z_value = QGD.find_z()
    con = sqlite3.connect("./stocks_DB.db")
    df = pd.read_sql("SELECT * FROM cap_company", con)
    con.close()
    context = {
        'ticker' : ticker,
        'data' : data.to_html(),
        'z_value' : round(z_value.values[0], 2),
        'market_cap': df.to_html(),
    }
    return render(request, "search/search_main.html", context=context)