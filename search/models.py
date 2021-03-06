from django.db import models
import yfinance as yf
import pandas as pd
import numpy as np

# Create your models here.
class QuantGaloreData:
    def __init__(self, Ticker):
        self.ticker = yf.Tickers(Ticker)
        self.data = yf.download(tickers=(Ticker),period='10y',interval='1d',group_by='ticker',auto_adjust=True,prepost=False)
        self.df = pd.DataFrame(self.data)
        # print(self.df.tail(1))
    def find_z(self):
        self.z_df = self.df[-251:]
        mean = self.z_df['Close'].mean()
        z_from_mean = (self.z_df['Close'].tail(1) - mean) / np.std(self.z_df['Close'])
        # print(self.ticker,self.df['Close'].tail(1),z_from_mean)

        return self.df, z_from_mean