from django import forms

from app.forms import RequestModelForm

from .models import User


class SignUpForm(RequestModelForm):
    name = forms.CharField(label="Seu nome", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Seu e-mail", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        ip_and_agent = self.get_ip_and_agent()
        user.ip = ip_and_agent.get('ip')
        user.agent = ip_and_agent.get('agent')
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    email = forms.EmailField(label="Seu e-mail", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
