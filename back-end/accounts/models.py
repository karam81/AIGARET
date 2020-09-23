from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, name, age, password=None, **extra_fields):
        try:
            user = self.model(
                username=username,
                name='fool',
                age=age,
            )
            print('name', name)
            extra_fields.setdefault('is_staff', False) 
            extra_fields.setdefault('is_superuser', False)
            user.set_password(password)
            user.is_active = True
            user.save(using=self._db)
            return user
        except Exception as e:
            print('에러', name)
            print(e)

    def create_superuser(self, username, age=0, name='superuser', password=None, **extra_fields):
        try:
            superuser = self.create_user(
                username=username,
                password=password,
                name=name,
                age=age,
            )
            superuser.is_admin = True
            superuser.is_superuser = True
            superuser.is_active = True
            superuser.is_staff = True
            superuser.save(using=self._db)
            return superuser
        except Exception as e:
            print(e)

class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    exercise_cycle = models.CharField(max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'age', 'exercise_cycle']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
