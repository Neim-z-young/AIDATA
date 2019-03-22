from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import AppUniqueUser, \
        TaskRelease, DataType, DataTwolType, DataSubmitAndCheck
from .forms import TaskReleaseForm, UserRegisterForm, UserLoginForm, \
        DataSubmitForm, DataCheckForm, DataTypeAddForm, DataTwolTypeAddForm
import requests


WECHAT_APPID = ''
WECHAT_SERCET = ''
def wechatLogin(request):
    """
    小程序登录
    """
    if request.method != 'GET':
        return HttpResponseBadRequest('错误请求')
    code = request.GET.get('code')
    form = requests.get("https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
        .format(WECHAT_APPID, WECHAT_SERCET, code)).json()
    if form['errcode']:
        return JsonResponse([form['errmsg']])
    openid = form['openid']
    user = authenticate(request, openid=openid)
    user.last_login_datetime = timezone.now()
    user.save()
    login(request, user)
    #返回session_key也行吧
    return JsonResponse({'msg': 'ok'})

def wechatTaskList(request):
    """
    小程序请求任务列表
    """
    if request.method == 'POST':
        taskList = list(TaskRelease.objects.all().values(
            'task_inc_id',
            'task_tag',
            'task_owner__username',
            'task_description',
            'task_data_num',
            'task_credits',
            'task_deadline',
            'task_onelevel_type__data_type_name',
            'task_twolevel_type__data_2ltype_name'
        ))
        return JsonResponse({'taskList': taskList}, safe=False)