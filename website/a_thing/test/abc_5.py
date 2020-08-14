from django import forms
# from django.contrib.auth.models import User


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

