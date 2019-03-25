from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail

#TODO 创建自定义用户管理
class AppCustomUserManager(BaseUserManager):
    """
    自定义用户管理, 重写创建用户方式
    """
    use_in_migrations = True

    def _create_user(self, email, password, username, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The email must to be set')
        if not username:
            username = email
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, username, **extra_fields)

class AppCustomUserWithWechatManager(AppCustomUserManager):
    """
    自定义用户管理, 重写创建用户方式
    """
    use_in_migrations = True
    
    def create_user(self, openid, email=None, password=None, username=None, **extra_fields):
        """
        Create and save a user with the given openid username, email, and password.
        """
        if not openid and not email:
            raise ValueError('The wechat openid must either to be set or the email')
        if not username:
            username = email if email else openid
        username = self.model.normalize_username(username)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        if email is None:
            user = self.model(wechat_open_id=openid, username=username, **extra_fields)
        else:
            email = self.normalize_email(email)
            user = self.model(wechat_open_id=openid, username=username, email=email, **extra_fields)
        user.username = 'ai'+ user.id
        user.set_password(password)
        user.save(using=self._db)
        return user

#TODO 创建自定义用户
class AppCustomUser(AbstractBaseUser):
    """
    自定义用户
    需要设置虚拟对象属性
    """
    username = models.CharField(
        _('app用户名, 可重名'),
        blank=True,
        null=True,
        max_length=150,
        help_text=_('网站用户名,最好不要包括奇奇怪怪的文字'),
        error_messages={},
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=True,
        blank=True,
        error_messages={
            'unique': _("当前邮件已被注册,请更换邮件或找回密码"),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    creat_datetime = models.DateTimeField(_('账号创建日期时间'), default=timezone.now)
    is_staff = models.BooleanField(
        _('网站员工'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('Web管理员'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('账号状态'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = AppCustomUserManager()

    class Meta:
        verbose_name = _('AppUser')
        abstract = True
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perms(self):
        """
        whether is admin
        """
        return self.is_active and self.is_superuser and self.is_staff
