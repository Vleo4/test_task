from django.db import models

from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from .user_manager import MenuUserManager


class MenuUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    USER_TYPE_CHOICES = (
        ('restaurant', 'Restaurant'),
        ('employee', 'Employee'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    name = models.CharField(max_length=150)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MenuUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "user_type"]

    class Meta:
        app_label = 'lunch_menu'
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.username

class MealMenu(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    menu_content = models.TextField()
    price = models.FloatField()
    restaurant = models.ForeignKey(MenuUser, verbose_name='Restaurant', on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    votes = models.ManyToManyField(MenuUser, blank=True, related_name='menu_votes')

    def __str__(self):
        return self.name