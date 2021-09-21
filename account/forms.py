from django import forms
from django.contrib.auth.models import User
from .models import Profile, AccountSettings
from django.utils.translation import gettext_lazy as _
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)

class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = AccountSettings
        fields = ('rotating_prayer_num','auto_pray', 'daily_email')
        labels = {
            'rotating_prayer_num': _('Daily rotating prayers'),
        }
