from django import forms
from django.forms import ModelForm

from watcher.models import Url

class UrlForm(ModelForm):
    # url = forms.URLField(label='URL', attrs={'required': True})
    # interval_type = forms.Select(
    #     attrs={'required': True},
    #     widget=forms.Select,
    #     choices=['second', 'minute', 'hour', 'day'],
    #     default='minute'
    # )
    # interval = forms.DecimalField(label='Interval', attrs={'required': True}, default=1)
    class Meta:
        model = Url
        fields = ['url', 'every', 'period',]
