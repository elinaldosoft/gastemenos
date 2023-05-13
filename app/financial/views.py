from django.views import View
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse


class DashboardView(View):
    template_name = "financial/dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)
