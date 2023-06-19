import uuid

from decimal import Decimal
from datetime import datetime, timedelta
from parameterized import parameterized

from django.test import TestCase

from app.accounts.models import User
from app.financial.models import Expense, TypeExpense


class TypeExpenseModelTest(TestCase):

    def setUp(self):
        super(TypeExpenseModelTest, self).setUp()
        self.type_expense = TypeExpense.objects.create(
            name="Moradia",
            description="Refere-se a aluguel, casa ou apartamento etc."
        )

    def test_create_type_expense(self):
        type_expense = TypeExpense.objects.create(
            name="Transporte",
            description="Meios de transporte"
        )

        self.assertGreaterEqual(type_expense.id, 1)
        self.assertEqual(type_expense.name, "Transporte")
        self.assertIsNotNone(type_expense.description)
        self.assertEqual(type_expense.created_at.strftime("%Y-%m-%d"), datetime.utcnow().strftime("%Y-%m-%d"))
        self.assertIsNone(type_expense.deleted_at)
        self.assertEqual(TypeExpense.objects.filter().count(), 2)

    def test_type_expense_not_exists(self):
        with self.assertRaises(TypeExpense.DoesNotExist):
            TypeExpense.objects.get(pk=-1)


class ExpenseModelTest(TestCase):
    def setUp(self):
        super(ExpenseModelTest, self).setUp()
        self.user = User.objects.create(code=uuid.uuid4(), name="User Teste Expense", email="teste@testexpense.com")
        self.type_expense = TypeExpense.objects.create(name="Vestuário", description="Roupas em geral")

    def test_status_expense(self):
        self.assertEqual(Expense.PAID, 'paid')
        self.assertEqual(Expense.PENDING, 'pending')
        self.assertEqual(Expense.OVERDUE, 'overdue')

    def test_create_expense(self):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            expires_at=datetime.utcnow() + timedelta(days=15),
            status=Expense.PENDING,
            type=self.type_expense,
            user=self.user,
        )

        self.assertGreaterEqual(expense.id, 1)
        self.assertEqual(expense.title, "Aluguel")
        self.assertEqual(expense.amount, Decimal("159.50"))
        self.assertEqual(
            expense.expires_at.strftime("%Y-%m-%d"),
            (datetime.utcnow() + timedelta(days=15)).strftime("%Y-%m-%d")
        )
        self.assertEqual(expense.status, "pending")
        self.assertIsNone(expense.notes)
        self.assertIsNone(expense.paid_at)
        self.assertEqual(expense.type, self.type_expense)
        self.assertEqual(expense.user_id, self.user.id)
        self.assertEqual(expense.user.name, "User Teste Expense")

    @parameterized.expand(
        [
            (Expense.PAID, "paid"),
            (Expense.OVERDUE, "overdue"),
        ]
    )
    def test_update_status_expense(self, status, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            expires_at=datetime.utcnow() + timedelta(days=15),
            status=Expense.PENDING,
            type=self.type_expense,
            user=self.user,
        )

        self.assertEqual(expense.status, "pending")

        expense.status = status
        expense.save()
        expense = Expense.objects.get(pk=expense.id)

        self.assertGreaterEqual(expense.id, 1)
        self.assertEqual(expense.status, excepted)

    @parameterized.expand(
        [
            (Expense.PENDING, datetime.today(), False),
            (Expense.PENDING, None, False),
            (Expense.OVERDUE, datetime.today(), False),
            (Expense.PAID, datetime.today(), True),
        ]
    )
    def test_is_paid(self, status, paid_at, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            status=status,
            paid_at=paid_at,
            expires_at=datetime.utcnow() + timedelta(days=5),
            type=self.type_expense,
            user=self.user,
        )

        result = expense.is_paid

        self.assertEqual(bool(result), excepted)

    @parameterized.expand(
        [
            (Expense.PENDING, datetime.today().date() - timedelta(days=5), True),
            (Expense.OVERDUE, datetime.today().date() - timedelta(days=5), True),
            (Expense.PAID, datetime.today().date() - timedelta(days=5), False),
        ]
    )
    def test_is_overdue(self, status, expires_at, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            status=status,
            expires_at=expires_at,
            type=self.type_expense,
            user=self.user,
        )

        result = expense.is_overdue

        self.assertEqual(bool(result), excepted)

    def test_expense_not_exists(self):
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(pk=-1)

    @parameterized.expand(
        [
            (Expense.PENDING, 'Pendente'),
            (Expense.OVERDUE, 'Vencido'),
            (Expense.PAID, 'Pago'),
            (None, 'Desconhecido'),
        ]
    )
    def test_get_status_display(self, status, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            status=status,
            expires_at=datetime.now().date(),
            type=self.type_expense,
            user=self.user,
        )

        result = expense.get_status_display()

        self.assertEqual(result, excepted)

    @parameterized.expand(
            [
                ('Pendente', Expense.PENDING,),
                ('Vencido', Expense.OVERDUE,),
                ('Pago', Expense.PAID,),
                ('Desconhecido', None),
            ]
    )
    def test_get_invert_status_display(self, status, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            status=status,
            expires_at=datetime.now().date(),
            type=self.type_expense,
            user=self.user,
        )

        result = expense.get_invert_status_display(status)

        self.assertEqual(result, excepted)
