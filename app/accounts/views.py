from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from .forms import SignUpForm


class AccountsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'accounts/index.html')

class SignUpView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = SignUpForm()
        return render(request, 'accounts/sign-up.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SignUpForm()
        return render(request, 'accounts/sign-up.html', {'form': form})
