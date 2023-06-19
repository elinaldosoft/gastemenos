from datetime import datetime, timedelta

from django import forms

from .models import Expense, TypeExpense


class ExpenseForm(forms.ModelForm):
    title = forms.CharField(label="Título", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    amount = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"class": "form-control"}))
    type = forms.ModelChoiceField(queryset=TypeExpense.objects.all(), label="Tipo Despesa")
    # expires_at = forms.DateField(label="Vencimento", widget=forms.DateInput(attrs={"class": "form-control", "id": "datepicker"}))
    expires_at = forms.DateField(widget=forms.SelectDateWidget(), initial=(datetime.now() + timedelta(days=32)).replace(day=1))
    # paid_at = forms.DateField(label="Está pago?", widget=forms.DateInput(attrs={"class": "form-control", "id": "datepicker_paid_at"}), required=False)
    paid_at = forms.DateField(label="Está pago?", widget=forms.SelectDateWidget(), required=False)
    status = forms.ChoiceField(label="Status", choices=Expense.STATUS_EXPENSE, required=False)
    notes = forms.CharField(label="Observações", widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}), required=False)

    class Meta:
        model = Expense
        fields = ['title', 'amount', 'type', 'expires_at', 'paid_at', 'status', 'notes']

class ExpenseDeleteForm(forms.ModelForm):
    id = forms.CharField(label="Id", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Expense
        fields = ['id']
