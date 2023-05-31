import uuid

from decimal import Decimal
from datetime import datetime, timedelta
from parameterized import parameterized

from django.test import TestCase

from app.accounts.models import User
from app.financial.models import Expense, TypeExpense, STATUS_EXPENSE


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
        self.assertEqual(STATUS_EXPENSE[0], ('paid', 'Pago'))
        self.assertEqual(STATUS_EXPENSE[1], ('pending', 'Pendente'))
        self.assertEqual(STATUS_EXPENSE[2], ('overdue', 'Vencida'))

    def test_create_expense(self):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            expires_at=datetime.utcnow() + timedelta(days=15),
            status=STATUS_EXPENSE[1][0],
            user=self.user,
        )

        expense.save()
        type_expense = self.type_expense
        expense.type_expense.add(type_expense)

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
        self.assertEqual(expense.type_expense.get(), type_expense)
        self.assertEqual(expense.user_id, self.user.id)
        self.assertEqual(expense.user.name, "User Teste Expense")

    @parameterized.expand(
        [
            (STATUS_EXPENSE[0][0], "paid"),
            (STATUS_EXPENSE[2][0], "overdue"),
        ]
    )
    def test_update_status_expense(self, status, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            expires_at=datetime.utcnow() + timedelta(days=15),
            status=STATUS_EXPENSE[1][0],
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
            (STATUS_EXPENSE[0][0], datetime.today(), True),
            (STATUS_EXPENSE[0][0], None, False),
            (STATUS_EXPENSE[1][0], datetime.today(), False),
            (STATUS_EXPENSE[2][0], datetime.today(), False),
        ]
    )
    def test_is_paid(self, status, paid_at, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            status=status,
            paid_at=paid_at,
            expires_at=datetime.utcnow() + timedelta(days=5),
            user=self.user,
        )

        result = expense.is_paid

        self.assertEqual(bool(result), excepted)

    @parameterized.expand(
        [
            (STATUS_EXPENSE[0][0], datetime.today() - timedelta(days=5), False),
            (STATUS_EXPENSE[1][0], datetime.today() - timedelta(days=5), True),
            (STATUS_EXPENSE[2][0], datetime.today() - timedelta(days=5), True),
        ]
    )
    def test_is_overdue(self, status, expires_at, excepted):
        expense = Expense.objects.create(
            title="Aluguel",
            amount=Decimal("159.50"),
            status=status,
            expires_at=expires_at,
            user=self.user,
        )

        result = expense.is_overdue

        self.assertEqual(bool(result), excepted)

    def test_expense_not_exists(self):
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(pk=-1)
