from django import forms

class SearchForm(forms.Form):
    """Search Form Definition"""
    ticker = forms.CharField(label=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['ticker'].widget.attrs.update({'class': 'searchbar'})


