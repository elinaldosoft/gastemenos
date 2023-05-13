from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from .forms import SignUpForm


class SignInView(LoginView):
    template_name = "accounts/sign-in.html"
    redirect_authenticated_user = True


class SignUpView(View):
    form_class = SignUpForm
    template_name = "accounts/sign-up.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("sign-in"))
        return render()
