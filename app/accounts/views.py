from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from .forms import SignUpForm


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
