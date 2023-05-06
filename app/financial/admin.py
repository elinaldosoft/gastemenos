from django.contrib import admin

from .models import TypeExpense, Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'expires_at', 'paid_at', 'status', 'user')
    list_filter = ('status', 'user')
    search_fields = ('title', 'user__name', 'user__email')

@admin.register(TypeExpense)
class TypeExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
