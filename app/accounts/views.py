import uuid

from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from app.utils import get_ip_and_agent

from .forms import SignUpForm, EditForm
from .models import User


class SignInView(LoginView):
    template_name = "accounts/sign-in.html"
    redirect_authenticated_user = True


class SignUpView(View):
    form_class = SignUpForm
    template_name = "accounts/sign-up.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect(reverse("sign-in"))
        return render()


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject'
    success_message = "Se o email informado na solicitação for o cadastrado no sistema você receberá um link para redefinição de senha caso contrário entre em contato." \
                      " suporte: gastemenos2023@gmail.com"
    success_url = reverse_lazy('home_page')


class EditAccountView(SuccessMessageMixin, PasswordResetView):
    form_class = EditForm
    template_name = 'accounts/edit_account.html'
    success_message = "Seus dados foram alterados com sucesso."
    success_url = reverse_lazy('home_page')

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect(reverse("dashboard"))
        return render(request, self.template_name)


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeView(request.POST, request=request)

        if form.is_valid():
            form.save()
            return redirect('sign-in')
    else:
        form = PasswordChangeView(request=request)

        args = {'form': form}
        return render(request, "password_change", args)


class DeleteAccountView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        messages.success(request, "Conta removida com sucesso.")
        email = f"{uuid.uuid4()}-disable@gastemenos.com"
        ip_agent = get_ip_and_agent(request)
        data = {
            'disable_ip': ip_agent.get('ip'),
            'disable_agent': ip_agent.get('agent'),
            'disable_email': request.user.email,
            'email': email,
            'disabled_at': timezone.now(),
        }
        User.objects.filter(id=request.user.id).update(**data)
        logout(request)
        return redirect(reverse("home_page"))
