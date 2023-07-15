import calendar
import locale
from datetime import datetime, timedelta

from django.db.models.functions import ExtractMonth
from django.views import View
from django.contrib import messages
from django.db.models import Q, Sum
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.utils import timezone

from .models import Expense, TypeExpense
from .forms import ExpenseForm
from .forms import ExpenseDeleteForm


class DashboardView(ListView):
    template_name = "financial/dashboard.html"
    paginate_by = 20
    model = Expense

    # def get_queryset(self):
    #     """
    #         https://www.postgresql.org/docs/current/datatype-textsearch.html
    #         tsvector search
    #     """
    #     query = super().get_queryset().filter(user=self.request.user)
    #     if search := self.request.GET.get('search'):
    #         query = query.annotate(search=SearchVector('title', 'notes')).filter(search=search)
    #     return query

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user)

        search = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if search:
            if search in ('Vencido', 'Pago', 'Pendente'):
                search = Expense.get_invert_status_display(self, search)

            query = query.filter(
                Q(title__iexact=search)
                | Q(status__iexact=search)
                | Q(type__name__iexact=search)
            )

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(expires_at__range=[start_date, end_date])
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


class ReportsView(View):
    def get(self, request, type_expense=None, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        if type_expense:
            expense_totals = Expense.objects.filter(
                user=request.user
            ).values('type__name').annotate(total=Sum('amount'))

            data = []
            labels = []

            for expense_total in expense_totals:
                type_name = expense_total['type__name']
                total_amount = expense_total['total']
                data.append(total_amount)
                labels.append(type_name)
            data_json = {'data': data, 'labels': labels}
        else:
            result = Expense.objects.filter(
                user=request.user, expires_at__gte=datetime.now() - timedelta(days=365)
            ).annotate(
                month=ExtractMonth('expires_at')
            ).values('month').annotate(total=Sum('amount'))

            data = []
            labels = []

            for entry in result:
                month = entry['month']
                month = calendar.month_abbr[month]
                total = entry['total']
                data.append(total)
                labels.append(month)
            data_json = {'data': data, 'labels': labels}

        return JsonResponse(data_json)
