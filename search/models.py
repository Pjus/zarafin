from django.db import models
import yfinance as yf
import pandas as pd
import numpy as np

# Create your models here.
class QuantGaloreData:
    def __init__(self, Ticker):
        self.ticker = yf.Tickers(Ticker)
        self.data = yf.download(tickers=(Ticker),period='1y',interval='1d',group_by='ticker',auto_adjust=True,prepost=False)
        self.df = pd.DataFrame(self.data)
        # print(self.df.tail(1))
    def find_z(self):
        mean = self.df['Close'].mean()
        z_from_mean = (self.df['Close'].tail(1) - mean) / np.std(self.df['Close'])
        # print(self.ticker,self.df['Close'].tail(1),z_from_mean)

        return self.df, z_from_mean