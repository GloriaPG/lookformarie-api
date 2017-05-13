# -*- coding: utf-8 -*-
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.core.mail import EmailMultiAlternatives

from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose

def upload_to_avatar(instance, filename):
    """
    Get the upload path to the profile image.
    """
    return '{0}/{1}{2}'.format(
        "avatars",
        md5(filename).hexdigest(),
        os.path.splitext(filename)[-1]
    )
class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo usuario.
    """

    def _create_user(
        self,
        email,
        password,
        is_superuser=False,
        is_staff=False,
        is_active=False,
        **extra_fields
    ):
        """
        Método base para la creación de nuevos usuarios.
        """
        if not email:
            raise ValueError('The given email address must be set.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea un nuevo usuario.
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea un nuevo usuario marcándolo como super usuario.
        """
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.TextField(
        max_length=50,
        blank=False,
        null=False
    )
    last_name = models.TextField(
        max_length=100,
        blank=True,
        null=True,
    )
    second_last_name = models.TextField(
        max_length=50,
        blank=True,
        null=True
    )
    bio = models.TextField(
        max_length=160,
        blank=True,
        null=True
    )
    data = models.TextField(
        max_length=250,
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        null=False
    )
    birthday = models.DateField(null=True)
    gender = models.TextField(
        max_length=50,
        blank=True,
        null=True)
    phone = models.TextField(
        max_length=20,
        blank=False,
        null=False
    )
    address = models.TextField(
        max_length=200,
        blank=False,
        null=False
    )
    avatar = models.ImageField(
        upload_to=upload_to_avatar,
        help_text="Elija imagen de logo (200x200)",
        verbose_name="Avatar",
        default="default.png"
    )

    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[Transpose(), ResizeToFill(200, 200)],
        format='PNG',
        options={'quality': 60}
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is_staff')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is_active')
    )
    register_date = models.DateField(
        auto_now=True,
    )

    last_modify_date = models.DateField(
        auto_now_add=True
    )
    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
        'phone',
        'is_active'
    ]

    def get_full_name(self):
        """
        Return full name user:
             name last_name second_last_name
        """
        parts = [self.name, self.last_name, self.second_last_name]
        return ' '.join(filter(None, parts))

    def get_short_name(self):
        """
        Return short name user:
            name last_name
        """
        parts = [self.name, self.last_name]
        return ' '.join(filter(None, parts))

    def email_user(self, subject, txt, html=None, from_email=None, **kwargs):
        """
        Send email to user.
        """
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        message = EmailMultiAlternatives(
            subject, txt, from_email, [self.email], **kwargs)

        if html is not None:
            message.attach_alternative(html, 'text/html')

        message.send()



class Keyword(models.Model):
    """docstring for ClassName"""
    keyword = models.TextField(
        max_length=100,
        blank=True,
        null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.keyword

class Resume(models.Model):
    title = models.TextField(max_length=250,null=False, blank=False)
    user = models.ForeignKey(User, null=False, related_name="user")
    date = models.DateTimeField(auto_now_add=False, auto_now=False, null=False)
    resume = models.TextField(max_length=250,null=False, blank=False)
    resume_file = models.FileField(upload_to='documents/%Y/%m/%d/', null=False)
    status = models.BooleanField(default=True)
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def __str__(self):              # __unicode__ on Python 2
        return self.title
