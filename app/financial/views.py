from datetime import datetime

from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils import timezone

from .models import Expense, TypeExpense
from .forms import ExpenseForm
from .forms import ExpenseDeleteForm


class DashboardView(ListView):
    template_name = "financial/dashboard.html"
    paginate_by = 20
    model = Expense

    def get_queryset(self):
        """
            https://www.postgresql.org/docs/current/datatype-textsearch.html
            tsvector search
        """
        query = super().get_queryset().filter(user=self.request.user)
        if search := self.request.GET.get('search'):
            query = query.annotate(search=SearchVector('title', 'notes')).filter(search=search)
        return query

    def post(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)


class FinancialView(View):
    template_name = "financial/new.html"
    form_class = ExpenseForm

    def get_object(self, pk: int = None) -> Expense:
        if pk and str(pk).isnumeric():
            return get_object_or_404(Expense, pk=pk, user=self.request.user)

    def get(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        expense = self.get_object(pk)
        form = self.form_class(instance=expense)
        return render(request, self.template_name, {'form': form, 'edit': True})

    def post(self, request: HttpRequest) -> HttpResponse:
        expense = self.get_object(request.POST.get('id'))
        form = self.form_class(request.POST, instance=expense)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user

            if form.paid_at:
                form.status = Expense.PAID
            elif not form.paid_at and form.expires_at < datetime.now().date():
                form.status = Expense.OVERDUE
            else:
                form.status = Expense.PENDING

            form.save()
            if expense:
                messages.success(request, "Despesa atualizada com sucesso.")
            else:
                messages.success(request, "Despesa criada com sucesso.")
            return redirect(reverse("dashboard"))
        return render(request, self.template_name)

class FinancialDeleteView(View):
    template_name = "financial/remove.html"
    form_class = ExpenseDeleteForm

    def get_object(self, pk: int = None) -> Expense:
        if pk and str(pk).isnumeric():
            return get_object_or_404(Expense, pk=pk, user=self.request.user)

    def get(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        expense = self.get_object(pk)
        form = self.form_class(instance=expense)
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        expense = self.get_object(request.POST.get('id'))
        form = self.form_class(request.POST, instance=expense)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.deleted_at = timezone.now()
            form.save()
            messages.success(request, "Despesa removida com sucesso.")            
            return redirect(reverse("dashboard"))
        return render(request, self.template_name)
