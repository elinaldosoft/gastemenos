from django import forms

from .models import User


class SignUpForm(forms.ModelForm):
    name = forms.CharField(label="Seu nome", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Seu e-mail", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class SignInForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
