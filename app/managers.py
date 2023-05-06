from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        user = super().create(**kwargs)
        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super().get_queryset()
