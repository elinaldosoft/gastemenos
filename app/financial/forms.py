from django import forms

from .models import Expense, TypeExpense


class ExpenseForm(forms.ModelForm):
    title = forms.CharField(label="Título", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Expense
        fields = ['title']
