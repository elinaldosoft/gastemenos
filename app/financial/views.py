import calendar
from collections import defaultdict
from datetime import datetime, timedelta

import openpyxl

from django.db.models.functions import ExtractMonth
from django.views import View
from django.contrib import messages
from django.db.models import Q, Sum
from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.utils import timezone

from .constants import LIMIT_DAYS_RANGE_IN_QUERY
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
            search_status = search.lower()
            if search_status in ('vencido', 'pago', 'pendente'):
                search = Expense.get_invert_status_display(self, search_status.capitalize())

            query = query.filter(
                Q(title__icontains=search)
                | Q(status__icontains=search)
                | Q(type__name__icontains=search)
            )

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if (end_date - start_date).days > LIMIT_DAYS_RANGE_IN_QUERY:
                start_date = None
                end_date = None
        else:
            today = datetime.today()
            start_date = datetime(today.year, today.month, 1)
            end_date = datetime(today.year, 12, 31)

        query = query.filter(expires_at__range=[start_date, end_date])

        return query

    def generate_excel_data(self, queryset):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        worksheet.append(['ID', 'Título', 'Tipo', 'Vencimento', 'Valor', 'Status', 'Pago em:'])

        type_expense_dict = defaultdict(str)

        type_expenses = TypeExpense.objects.all()

        for type_expense in type_expenses:
            type_expense_dict[type_expense.id] = type_expense.name

        status_dict = dict(Expense.STATUS_EXPENSE)

        for expense in queryset:
            worksheet.append(
                [
                    expense.id,
                    expense.title,
                    type_expense_dict[expense.type_id],
                    expense.expires_at,
                    'R$ ' + str(expense.amount).replace('.', ','),
                    status_dict.get(expense.status, ('Desconhecido')),
                    expense.paid_at.strftime('%Y-%m-%d') if expense.paid_at else None,
                ]
            )

        return workbook

    def download_excel(self, request, queryset):
        workbook = self.generate_excel_data(queryset)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=despesas.xlsx'
        workbook.save(response)

        return response

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        generate_excel = self.request.GET.get('generate_excel')
        if generate_excel == 'true':
            response = self.download_excel(request, queryset)
            return response

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            context['start_date'] = start_date
            context['end_date'] = end_date
            diff_dates = datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.strptime(start_date, '%Y-%m-%d').date()

            if diff_dates.days > LIMIT_DAYS_RANGE_IN_QUERY:
                context['error_message'] = "A diferença entre as datas não pode ser superior a 1 ano."
        else:
            today = datetime.today()
            context['start_date'] = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
            context['end_date'] = datetime(today.year, 12, 31).strftime('%Y-%m-%d')

        return context

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
                user=request.user, expires_at__gte=timezone.now() - timedelta(days=365)
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
