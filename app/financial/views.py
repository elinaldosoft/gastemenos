from django.views import View
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from .forms import ExpenseForm


class DashboardView(View):
    template_name = "financial/dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

class FinancialView(View):
    template_name = "financial/new.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ExpenseForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)
