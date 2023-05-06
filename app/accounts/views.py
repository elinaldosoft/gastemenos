from django.shortcuts import render
from django.views import View


class AccountsView(View):
    def get(self, request):
        return render(request, 'accounts/index.html')

    def post(self, request):
        return render(request, 'accounts/index.html')
