from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import TaskRelease, DataSubmitAndCheck, AppUniqueUser, DataType, DataTwolType

class AdminLoginForm(forms.Form):
    adminName = forms.CharField(label='Admin name', max_length=150)
    adminPassword = forms.CharField(label='Admin password', max_length=128, widget=forms.PasswordInput)

#用户注册
class UserRegisterForm(forms.Form):
    email = forms.EmailField(label='邮件', required=True)
    username = forms.CharField(label='用户名', max_length=150)
    password = forms.CharField(label='密码', max_length=128, widget=forms.PasswordInput, required=True)
    confirmPassword = forms.CharField(label='确认密码', max_length=128, widget=forms.PasswordInput, required=True)
        

#用户登录表单
class UserLoginForm(forms.Form):
    userEmail = forms.EmailField(label='User Email')
    userPassword = forms.CharField(label='User password', max_length=128, widget=forms.PasswordInput)

class TaskReleaseForm(ModelForm):
    class Meta:
        model = TaskRelease
        fields = ['task_tag', 'task_description', 'task_data_num',
            'task_credits', 'task_deadline', 'task_onelevel_type',
            'task_twolevel_type']
        labels = {
            'task_tag': _('任务标签'),
            'task_description': _('任务描述'),
            'task_onelevel_type': _('任务一级数据类型'),
            'task_twolevel_type': _('任务二级数据类型'),
        }
        widgets = {
            'task_description': forms.Textarea(attrs={'cols': 25, 'rows': 6}),
        }
        error_messages = {
            'task_onelevel_type': {
                'required': _('数据类型不能为空'),
            },
            'task_twolevel_type': {
                'required': _('数据类型不能为空'),
            }
        }

#修改为DataSubmitAndCheckForm的子类
class DataSubmitForm(ModelForm):
    
    class Meta:
        model = DataSubmitAndCheck
        fields = ['temp_data_file', 'data_description']
        labels = {
            'temp_data_file' : '文件',
            'data_description' : '文件描述'
        }
        widgets = {
            'temp_data_file' : forms.ClearableFileInput(attrs={'multiple' : True}),
            'data_description' : forms.Textarea(attrs={'cols': 25, 'rows': 6}),
        }
        error_messages = {
            'data_description' : {
                'max_length': _('数据描述不超过75个字'),
            },
        }

class DataCheckForm(ModelForm):

    class Meta:
        model = DataSubmitAndCheck
        fields = ['data_check_state', 'data_check_description']
        #exclude = ['data_inc_id', 'data_owner_id']
        labels = {
            'data_check_state' : _('数据审核状态'),
            'data_check_description' : _('数据审核描述')
        }
        widgets = {
            'data_check_state' : forms.Select(choices=[('checking', 'CHECKING'), ('passed', 'PASSED'), ('failed', 'FAILED')]),
            'data_check_description' : forms.Textarea(attrs={'cols': 25, 'rows': 6}),
        }
        help_text = {
            'data_check_description' : _('数据审核状态原因描述'),
        }

class DataTypeAddForm(ModelForm):
    class Meta:
        model = DataType
        fields = ['data_type_name', 'data_type_description']
        labels = {
            'data_type_name': _('数据类型名'),
            'data_type_description': _('类型描述'),
        }
        widgets = {
            'data_type_description': forms.Textarea(attrs={'cols': 25, 'rows': 6}),
        }

class DataTwolTypeAddForm(ModelForm):
    class Meta:
        model = DataTwolType
        fields = ['belongto_data_type', 'data_2ltype_name', 'data_2ltype_description']
        labels = {
            'belongto_data_type': _('所属一级类型'),
            'data_2ltype_name': _('二级类型名'),
            'data_2ltype_description': _('二级类型描述'),
        }
        widgets = {
            'data_2ltype_description': forms.Textarea(attrs={'cols': 25, 'rows': 6}),
        }
 
