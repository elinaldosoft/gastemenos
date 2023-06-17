from django import forms

from .models import Expense, STATUS_EXPENSE, TYPE_EXPENSE


class ExpenseForm(forms.ModelForm):
    title = forms.CharField(label="Título", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    amount = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"class": "form-control"}))
    type = forms.ChoiceField(label="Tipo", choices=TYPE_EXPENSE)
    expires_at = forms.DateField(label="Vencimento", widget=forms.DateInput(attrs={"class": "form-control", "id": "datepicker"}))
    paid_at = forms.DateField(label="Está pago?", widget=forms.DateInput(attrs={"class": "form-control", "id": "datepicker_paid_at"}), required=False)
    status = forms.ChoiceField(label="Status", choices=STATUS_EXPENSE)
    notes = forms.CharField(label="Observações", widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}), required=False)

    class Meta:
        model = Expense
        fields = ['title', 'amount','type', 'expires_at', 'paid_at', 'status', 'notes']

class ExpenseDeleteForm(forms.ModelForm):
    id = forms.CharField(label="Id", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Expense
        fields = ['id']
