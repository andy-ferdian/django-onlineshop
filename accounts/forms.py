from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from store.models import Customer


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)


class UpdateUserForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value = True))

    class Meta:
        model = User
        fields = ("username", "email",
                  "password",)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'email', 'phone']
