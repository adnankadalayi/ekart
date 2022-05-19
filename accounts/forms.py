from . models import Accounts, Address
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


class RegistraionForm(forms.ModelForm):
    password = forms.CharField( widget=forms.PasswordInput(attrs={
      'class' : 'form-control',
    }))
    confirm_password = forms.CharField( widget=forms.PasswordInput(attrs={
      'class' : 'form-control',
    }))
    class Meta:
        model = Accounts
        fields = ['first_name', 'last_name', 'username','email','phone_no','password']

    def __init__(self, *args, **kwargs):
        super(RegistraionForm, self).__init__(*args, **kwargs)
      
        # looping in every field to place class form-control
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            

    def clean(self):
        cleaned_data = super(RegistraionForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError('Password not match')

class UserProfileUpdateForm(UserChangeForm):
    password = None
    class Meta:
      model = Accounts
      fields = ['first_name', 'last_name', 'username','email','phone_no']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
              self.fields[field].widget.attrs['class'] = 'form-control'

class UserAddressUpdateForm(UserChangeForm):
    class Meta:
      model = Address
      fields = '__all__'
      
    def __init__(self, *args, **kwargs):
        super(UserAddressUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
              self.fields[field].widget.attrs['class'] = 'form-control'
    
    
class UserPasswordForm(PasswordChangeForm):
      
    def __init__(self, *args, **kwargs):
        super(UserPasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields:
              self.fields[field].widget.attrs['class'] = 'form-control'
              self.fields[field].widget.attrs['type'] = 'password'
    