from django import forms

class SearchForm(forms.Form):
    """Search Form Definition"""
    ticker = forms.CharField()
    