from django.shortcuts import render
from . import forms
from .models import *
import sqlite3
import json

# bokeh
from bokeh.embed import components

import bokeh
import holoviews as hv
from bokeh.sampledata.stocks import AAPL
from holoviews.plotting.links import RangeToolLink
from holoviews import opts

# Create your views here.
def search(request):
    ticker = request.GET.get('ticker').upper()
    QGD = QuantGaloreData(Ticker=ticker)
    prices, z_value = QGD.find_z()
    prices['Date'] = prices.index
    # print(prices)
    con = sqlite3.connect("./stocks_DB.db")
    market_cap = pd.read_sql("SELECT * FROM cap_company", con)

    fcf = pd.read_sql(f"SELECT * FROM '{ticker}_fcf_Q'", con, index_col='index')
    fcf.drop(['Ticker', 'Freq'], axis=1, inplace=True)

    ratios = pd.read_sql(f"SELECT * FROM '{ticker}_FR_Q'", con, index_col='index')
    ratios.drop(['Ticker', 'Freq'], axis=1, inplace=True)

    company_name = market_cap[market_cap['Ticker']==ticker]['Name']
    con.close()

    hv.extension('bokeh')
    renderer = hv.renderer('bokeh')

    # Make dataframe from stock data
    aapl_df = pd.DataFrame(prices['Close'], columns=['Close'], index=pd.to_datetime(prices['Date']))
    aapl_df.index.name = 'Date'

    # Create stock curve
    aapl_curve = hv.Curve(aapl_df, 'Date', ('Close', 'Price ($)'))
    # Labels and layout
    tgt = aapl_curve.relabel(f'{ticker} close price').opts(width=800, labelled=['y'], toolbar='disable')
    src = aapl_curve.opts(width=800, height=100, yaxis=None, default_tools=[])

    RangeToolLink(src, tgt)
    # Merge rangetool
    layout = (tgt + src).cols(1)
    layout.opts(opts.Layout(shared_axes=False, merge_tools=False))

    html = renderer.html(layout)
    print(company_name.values)

    context = {
        'name': company_name.values[0],
        'ticker' : ticker,
        'prices' : prices.to_html(),
        'z_value' : round(z_value.values[0], 2),
        'market_cap': market_cap.to_html(),
        'free_cash_flow' : fcf.T.to_html(),
        'key_ratios': ratios.T.to_html(),
        'html':html,
    }
    return render(request, "search/search_main.html", context=context)