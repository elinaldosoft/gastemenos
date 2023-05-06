from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from .forms import SignUpForm


class SignInView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/sign-in.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/sign-in.html')


class SignUpView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = SignUpForm()
        return render(request, 'accounts/sign-up.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'accounts/sign-up.html', {'form': form})
