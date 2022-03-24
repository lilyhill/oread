from django import forms

class HighlightForm(forms.Form):

    anchorNode = forms.CharField(max_length=1000, )
    anchorOffset = forms.IntegerField()
    color = forms.CharField(max_length=1000, )
    container = forms.CharField(max_length=10000, )
    focusNode = forms.CharField(max_length=10000, )
    focusOffset = forms.CharField(max_length=10000, )
    href = forms.URLField()
    string = forms.CharField(max_length=1000000,) # Alias for string
    textColor = forms.CharField(max_length=1000, required=False)
    uuid = forms.CharField(max_length=100, )
    version = forms.CharField(max_length=100, )