from django.contrib.auth.models import User
from django import forms
from .models import Profile

import phonenumbers
from phonenumbers import NumberParseException


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    phone = forms.CharField(label='phone', max_length=15)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'phone')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # def clean_phone(self):
    #     cd = self.cleaned_data
    #     return cd['phone']
    #     # return "Not working, this should be shown the phone number"
    #     # return self.phone

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class BootstrapInput(forms.TextInput):
    def __init__(self, placeholder, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapInput, self).__init__(attrs={
            'class': 'form-control input-sm',
            'placeholder': placeholder
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapInput, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class BootstrapSelect(forms.Select):
    def __init__(self, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapSelect, self).__init__(attrs={
            'class': 'form-control input-sm',
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n}'.format(n=self.size)

        return '''
                <div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                <div>
                '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapSelect, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class VerificationForm(forms.Form):
    # country_code = forms.CharField(
    #     widget=BootstrapInput('Country Code', size=3)
    # )
    # phone_number = forms.CharField(
    #     widget=BootstrapInput('Phone Number', size=6)
    # )
    via = forms.ChoiceField(
        choices=[('sms', 'SMS'), ('call', 'Call')],
        widget=BootstrapSelect(size=3)
    )

    # def clean_country_code(self):
    #     country_code = self.cleaned_data['country_code']
    #     if not country_code.startswith('+'):
    #         country_code = '+' + country_code
    #     return country_code
    #
    # def clean(self):
    #     data = self.cleaned_data
    #     phone_number = data['country_code'] + data['phone_number']
    #     try:
    #         phone_number = phonenumbers.parse(phone_number, None)
    #         if not phonenumbers.is_valid_number(phone_number):
    #             self.add_error('phone_number', 'Invalid phone number')
    #     except NumberParseException as e:
    #         self.add_error('phone_number', e)


class TokenForm(forms.Form):
    token = forms.CharField(
        widget=BootstrapInput('Verification Token', size=6))

