from django import forms
from django.contrib.auth.models import User
 
class RegistrationForm(forms.Form):
    username=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),label='')
    
    def clean(self):
      email=self.cleaned_data.get("email")
      email_qs = User.objects.all().filter(email=email)
      username = self.cleaned_data.get("username")
      username_qs = User.objects.all().filter(username=username)
      password1=self.cleaned_data.get("password1")
      password2=self.cleaned_data.get("password2")

      if not 'iitbhu.ac.in' in email and not 'itbhu.ac.in' in email:
      	raise forms.ValidationError('You are not eligible to register. You are not a student of IITBHU')
      if email_qs.exists():
        raise forms.ValidationError("Email already exists")

      if password1!=password2:
        raise forms.ValidationError("Password must match")
      return super(RegistrationForm,self).clean()
    
    def save(self, new_data):
        u = User.objects.create_user(username=new_data['email'],
                                     first_name=new_data['username'],
                                     email=new_data['email'],
                                     password=new_data['password1'])
        u.is_active = False
        u.save()
        return u

class LoginUserForm(forms.Form):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),label='')
