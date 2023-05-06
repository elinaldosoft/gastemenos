from django import forms


class SignUpForm(forms.Form):
    name = forms.CharField(label="Seu nome", max_length=100)
    email = forms.EmailField(label="Seu e-mail", max_length=100)
    password = forms.PasswordInput()


class SignInForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)