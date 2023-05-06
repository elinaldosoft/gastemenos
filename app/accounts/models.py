import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from app.models import BaseModel
from app.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    code = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Código do Aluno', unique=True)
    name = models.CharField(max_length=255, verbose_name=_('Nome'), null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, error_messages={'unique': 'Usuário com e-mail já existente.'})
    phone = models.CharField(max_length=255, verbose_name=_('Telefone'), blank=True, null=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
        verbose_name='Acesso ao Dashboard?',
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        verbose_name='Ativo?',
    )
    username = None

    USERNAME_FIELD = 'email'
    last_login = None

    objects = UserManager()
