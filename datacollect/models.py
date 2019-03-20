from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import os.path
from datetime import timedelta

from .customUser import AppCustomUser, AppCustomUserWithWechatManager

def user_directory_path(instance, filename):
    """
    file will be uploaded to
    MEDIA_ROOT/temp_new/user_<id>/task_<task_id>_tag_<task_tag>/<filename>
    """
    return 'temp_new/user_{0}/task_{1}_tag_{2}/{3}'.format(instance.data_owner_id,
            instance.data_task.task_inc_id, instance.data_task.task_tag, filename)


#class AppUniqueUser(AbstractUser):
#     """
#     存放app中已实名认证的用户
#     """
#     wechat_open_id = models.CharField(max_length=20, unique=True, null=True, blank=True,
#         verbose_name='微信openid')
#     user_creat_datetime = models.DateTimeField(blank=True, null=True,
#         verbose_name='app用户账号创建日期时间')
#     user_last_login_datetime = models.DateTimeField(blank=True, null=True,
#         verbose_name='app用户上次登录日期时间')
#     # user_is_vip = models.BooleanField(
#     #     _('用户会员制/权限'),
#     #     default=False,
#     #     help_text=_('区别用户是否可以添加任务'),
#     # )
#     tasks_accepted = models.ManyToManyField('TaskRelease',
#         db_table='users_tasks_accepted',
#         verbose_name='app用户领取的任务集合'
#         )
#   
#     class Meta:
#         verbose_name = "普通用户"

class AppUniqueUser(AppCustomUser):
    """
    存放app中认证的用户
    """
    wechat_open_id = models.CharField(max_length=20, unique=True, null=True, blank=True,
        verbose_name='微信openid')
    last_login_datetime = models.DateTimeField(blank=True, null=True,
        verbose_name='app用户上次登录日期时间')
    tasks_accepted = models.ManyToManyField('TaskRelease',
        db_table='users_tasks_accepted',
        verbose_name='app用户领取的任务集合'
        )
    
    objects = AppCustomUserWithWechatManager()
    class Meta:
        verbose_name = "普通用户"

class DataType(models.Model):
    """
    数据一级类型表，标识数据的大类划分，如图片/音频等
    """
    data_type_id = models.AutoField(primary_key=True,
        verbose_name='自增ID')
    data_type_owner = models.ForeignKey(AppUniqueUser, on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name='数据类型创建者')
    data_type_name = models.CharField(max_length=10, unique=True,
        verbose_name='数据类型名，如“image”、“voice”')
    data_type_description = models.CharField(max_length=30, blank=True, null=True,
        verbose_name='数据类型描述')
    data_type_add_datetime = models.DateTimeField(default=timezone.now,
        verbose_name='数据类型添加日期时间')

    def __str__(self):
        return self.data_type_name
    class Meta:
        verbose_name = "数据一级类型"

class DataTwolType(models.Model):
    """
    二级数据类型信息
    """
    data_2ltype_id = models.AutoField(primary_key=True,
        verbose_name='自增ID')
    data_2ltype_owner = models.ForeignKey(AppUniqueUser, on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name='二级类型创建者')
    belongto_data_type = models.ForeignKey(DataType, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='二级数据类型所属一级数据类型')
    data_2ltype_name = models.CharField(max_length=20,
        verbose_name='二级数据类型名')
    data_2ltype_description = models.CharField(max_length=40, blank=True, null=True,
        verbose_name='二级数据类型描述')
    data_2ltype_add_datetime = models.DateTimeField(default=timezone.now,
        verbose_name='二级数据类型添加日期时间')

    def __str__(self):
        return self.data_2ltype_name
    class Meta:
        verbose_name = "数据二级类型"


#TODO 添加一个任务所需数据量的字段, 以及任务积分
class TaskRelease(models.Model):
    """
    任务发布
    """
    task_inc_id = models.AutoField(primary_key=True,
        verbose_name='任务id')
    task_tag = models.CharField(max_length=20,
        verbose_name='任务标签')
    task_description = models.CharField(max_length=50, blank=True, null=True,
        verbose_name='任务具体内容描述')
    task_data_num = models.PositiveIntegerField(default=20,
        verbose_name='任务所需数据量')
    task_credits = models.PositiveIntegerField(default=30,
        verbose_name='任务积分')
    #task_deadline = models.DurationField(default=time)
    task_deadline = models.DateTimeField(default=timezone.now()+timedelta(days=1),
        verbose_name='任务时限')
    task_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='任务创建者')
    task_onelevel_type = models.ForeignKey(DataType, on_delete=models.CASCADE,
        verbose_name='任务所需数据的一级类型')
    task_twolevel_type = models.ForeignKey(DataTwolType, on_delete=models.CASCADE,
        verbose_name='任务所需数据的二级类型')
    task_create_datetime = models.DateTimeField(default=timezone.now,
        verbose_name='任务创建日期时间')
    task_finish_state = models.CharField(max_length=10, blank=True, null=True,
        verbose_name='任务完成状态')

    def __str__(self):
        return self.task_tag
    class Meta:
        verbose_name = "任务发布表"


class DataSubmitAndCheck(models.Model):
    """
    用户提交数据进入后台审核阶段，对数据标注状态
    """
    data_inc_id = models.AutoField(primary_key=True,
        verbose_name='数据自增id')
    temp_data_file = models.FileField(upload_to=user_directory_path,
        verbose_name='数据在服务器中的暂存路径,包括数据名，由用户提交时确定')
    data_owner = models.ForeignKey(AppUniqueUser, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='数据所有者')
    data_task = models.ForeignKey(TaskRelease, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='数据所属任务')
    data_description = models.CharField(max_length=50, blank=True, null=True,
        verbose_name='用户数据描述')
    data_submit_datetime = models.DateTimeField(default=timezone.now,
        verbose_name='数据提交日期时间')
    data_check_state = models.CharField(max_length=10, blank=True, null=True,
        verbose_name='数据审核状态，可以为“通过”、“未通过”、“待审核”等等')
    data_check_description = models.CharField(max_length=30, blank=True, null=True,
        verbose_name='数据审核描述，如对未通过数据的原因说明')
    
    def fileName(self):
        return os.path.basename(self.temp_data_file.name)
    class Meta:
        verbose_name = "数据提交并审核"

class PictureSubmitted(models.Model):
    """
    已提交的图片存放表, 按大类存放
    """
    data_id = models.AutoField(primary_key=True,
        verbose_name='图片在数据库中的自增ID')
    data_image_file = models.FileField(upload_to=user_directory_path,
        verbose_name='图片路径，由开头定义的变量确定,包括图片名')
    data_owner = models.ForeignKey(AppUniqueUser, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='数据所有者')
    data_description = models.CharField(max_length=50, blank=True, null=True,
        verbose_name='图片描述')
    data_task = models.ForeignKey(TaskRelease, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='数据所属任务id')
    data_submit_datetime = models.DateTimeField(blank=True, null=True,
        verbose_name='图片提交日期时间')
   
    class Meta:
        verbose_name = "已提交的图片存放表"
