from django.shortcuts import render
from . import forms
from .models import *
import sqlite3
import json

# Create your views here.
def search(request):
    if request.GET.get('financial') == 'True':
        print('finance')
    ticker = request.GET.get('ticker').upper()
    QGD = QuantGaloreData(Ticker=ticker)
    prices, z_value = QGD.find_z()
    prices['Date'] = prices.index
    prices['Date'] = prices['Date'].astype(str)

    con = sqlite3.connect("./stocks_DB.db")
    market_cap = pd.read_sql("SELECT * FROM cap_company", con)

    fcf = pd.read_sql(f"SELECT * FROM '{ticker}_fcf_Q'", con, index_col='index')
    fcf.drop(['Ticker', 'Freq'], axis=1, inplace=True)

    ratios = pd.read_sql(f"SELECT * FROM '{ticker}_FR_Q'", con, index_col='index')
    ratios.drop(['Ticker', 'Freq'], axis=1, inplace=True)

    company_name = market_cap[market_cap['Ticker']==ticker]['Name']
    con.close()
    closes = [round(x, 2) for x in prices['Close'].to_list()]
    date = prices['Date'].to_list()
    date = [x.replace("&quot;", "") for x in date]
    temp = ratios[0:1]
    temp_dict = {}
    for i in temp:
        temp_dict[i] = temp[i][0]

    context = {
        'name': company_name.values[0],
        'ticker' : ticker,
        'date' : json.dumps(date),
        'prices' : prices.to_html(),
        'close' : json.dumps(closes),
        'z_value' : round(z_value.values[0], 2),
        'market_cap': market_cap.to_html(),
        'free_cash_flow' : fcf.T.to_html(),
        'key_ratios': temp_dict,
    }
    return render(request, "search/search_main.html", context=context)


def finance(request, ticker):

    QGD = QuantGaloreData(Ticker=ticker)
    prices, z_value = QGD.find_z()
    prices['Date'] = prices.index
    prices['Date'] = prices['Date'].astype(str)

    con = sqlite3.connect("./stocks_DB.db")
    market_cap = pd.read_sql("SELECT * FROM cap_company", con)

    fcf = pd.read_sql(f"SELECT * FROM '{ticker}_fcf_Q'", con, index_col='index')
    fcf.drop(['Ticker', 'Freq'], axis=1, inplace=True)

    ratios = pd.read_sql(f"SELECT * FROM '{ticker}_FR_Q'", con, index_col='index')
    ratios.drop(['Ticker', 'Freq'], axis=1, inplace=True)

    company_name = market_cap[market_cap['Ticker']==ticker]['Name']
    con.close()
    closes = [round(x, 2) for x in prices['Close'].to_list()]
    date = prices['Date'].to_list()
    date = [x.replace("&quot;", "") for x in date]
    temp = ratios[0:1]
    temp_dict = {}
    for i in temp:
        temp_dict[i] = temp[i][0]

    context = {
        'name': company_name.values[0],
        'ticker' : ticker,
        'date' : json.dumps(date),
        'prices' : prices.to_html(),
        'close' : json.dumps(closes),
        'z_value' : round(z_value.values[0], 2),
        'market_cap': market_cap.to_html(),
        'free_cash_flow' : fcf.T.to_html(),
        'key_ratios': temp_dict,
    }

    return render(request, "search/finance.html", context=context)