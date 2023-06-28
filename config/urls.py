"""
URL configuration for gastemenos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from functools import partial

from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from app.accounts.views import SignInView, SignUpView, ResetPasswordView
from app.financial.views import DashboardView, FinancialView, FinancialDeleteView, ReportsView

report_type_expense = partial(ReportsView.as_view(), type_expense='type_expense')

urlpatterns = [
    path(
        "", RedirectView.as_view(url="sign-in", permanent=False), name="home_page"
    ),  # Redirect to sign-in
    path("sign-in", SignInView.as_view(), name="sign-in"),
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path("logout", login_required(auth_views.LogoutView.as_view()), name="logout"),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "nova", login_required(FinancialView.as_view()), name="create_or_edit_expense"
    ),
    path(
        "conta/<int:pk>", login_required(FinancialView.as_view()), name="edit_expense"
    ),
    path(
        "conta/remove",
        login_required(FinancialDeleteView.as_view()),
        name="delete_expense_confirm",
    ),
    path(
        "conta/remove/<int:pk>",
        login_required(FinancialDeleteView.as_view()),
        name="delete_expense",
    ),
    path("dashboard", login_required(DashboardView.as_view()), name="dashboard"),
    path("report_expense", login_required(ReportsView.as_view()), name="report_expense"),
    path("report_type_expense", report_type_expense, name="report_type_expense"),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Gaste Menos ®"
admin.site.site_title = "Gaste Menos ®"
admin.site.index_title = "Gaste Menos ®"
