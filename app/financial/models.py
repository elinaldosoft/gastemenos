from django.db import models

from app.models import BaseModel


class TypeExpense(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de Despesa'
        verbose_name_plural = 'Tipos de Despesas'


class Expense(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Título')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    expires_at = models.DateField(verbose_name='Vencimento')
    paid_at = models.DateField(verbose_name='Pago em', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Status', null=True, blank=True, choices=(
        ('paid', 'Pago'),
        ('pending', 'Pendente'),
        ('overdue', 'Vencida'),
    ))
    notes = models.TextField(verbose_name='Observações', null=True, blank=True)
    type_expense = models.ManyToManyField(TypeExpense, verbose_name='Tipo de Despesa')
    user = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, verbose_name='Usuário')

    def __str__(self) -> str:
        return f"{self.id} | {self.title}"

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'