from datetime import datetime

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
    PENDING, OVERDUE, PAID = "pending", "overdue", "paid"
    STATUS_EXPENSE = (
        (PENDING, 'Pendente'),
        (OVERDUE, 'Vencido'),
        (PAID, 'Pago'),
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    expires_at = models.DateField(verbose_name='Vencimento')
    paid_at = models.DateField(verbose_name='Pago em', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Status', null=True, blank=True, choices=STATUS_EXPENSE)
    notes = models.TextField(verbose_name='Observações', null=True, blank=True)
    type = models.ForeignKey('financial.TypeExpense', on_delete=models.DO_NOTHING, verbose_name='Tipo de Despesa', related_name="expenses", default='')
    user = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, verbose_name='Usuário')

    def __str__(self) -> str:
        return f"{self.id} | {self.title}"

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-created_at']

    @property
    def is_paid(self) -> bool:
        return self.status == self.PAID and self.paid_at

    @property
    def is_overdue(self) -> bool:
        return self.status != self.PAID and self.expires_at < datetime.now().date()

    def get_status_display(self):
        status_dict = dict(self.STATUS_EXPENSE)
        return status_dict.get(self.status, ('Desconhecido'))
