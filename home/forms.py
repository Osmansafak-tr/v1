from django import forms

from .models import arastırmacı

class yayinCreateForm(forms.Form):
    yayin_ismi = forms.CharField()
    yayin_yili = forms.CharField()
    yazarlar = forms.CharField()
    yayin_yeri = forms.CharField()
    yayin_türü = forms.CharField()