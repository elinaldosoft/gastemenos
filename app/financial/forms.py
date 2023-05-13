from django import forms

from .models import Expense, STATUS_EXPENSE


class ExpenseForm(forms.ModelForm):
    title = forms.CharField(label="Título", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    amount = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"class": "form-control"}))
    expires_at = forms.DateField(label="Vencimento", widget=forms.DateInput(attrs={"class": "form-control", "id": "datepicker"}))
    status = forms.ChoiceField(label="Status", choices=STATUS_EXPENSE)
    notes = forms.CharField(label="Observações", widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}), required=False)

    class Meta:
        model = Expense
        fields = ['title', 'amount', 'expires_at', 'status', 'notes']
