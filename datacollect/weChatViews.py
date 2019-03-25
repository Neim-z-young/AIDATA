from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import AppUniqueUser, \
        TaskRelease, DataType, DataTwolType, DataSubmitAndCheck
from .forms import TaskReleaseForm, DataSubmitForm, DataCheckForm
import requests


WECHAT_APPID = 'wxea7bb1aaa082ef97'
WECHAT_SERCET = '6ef9cbe4f5ab1b1d49ecf6a26efd6783'
def wechatLogin(request):
    """
    小程序登录
    """
    if request.method != 'GET':
        return HttpResponseBadRequest('错误请求')
    code = request.GET.get('code')
    form = requests.get("https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
        .format(WECHAT_APPID, WECHAT_SERCET, code)).json()
    print(form)
    if 'errcode' in form:
        return JsonResponse({'errmsg': form['errmsg']})
    openid = form['openid']
    user = authenticate(request, openid=openid)
    user.last_login_datetime = timezone.now()
    user.save()
    login(request, user)
    #返回session_key也行吧
    return JsonResponse({'msg': 'ok'})

@login_required
def wechatTaskList(request):
    """
    小程序请求任务列表
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('错误请求')
    user = request.user
    pk_values = user.tasks_accepted.values_list('pk', flat=True)
    #连接查询,效率较低,可以优化
    taskList = list(TaskRelease.objects.all().exclude(pk__in=list(pk_values)).exclude(task_owner=user).values(
        'task_inc_id',
        'task_tag',
        'task_owner__username',
        'task_description',
        'task_data_num',
        'task_credits',
        'task_deadline',
        'task_onelevel_type__data_type_name',
        'task_twolevel_type__data_2ltype_name',
        'task_create_datetime'
    ))
    return JsonResponse({'taskList': taskList}, safe=False)

@login_required
def wechatUserTaskAccepting(request):
    """
    由任务id接受新任务
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('错误请求')
    taskId = request.POST.get('taskId')
    user = request.user
    task = user.tasks_accepted.all().filter(pk=taskId)
    if task.count() == 0:
        try:
            task = TaskRelease.objects.get(pk=taskId)
        except TaskRelease.DoesNotExist:
            msg = {'msg': 'task does not exist'}
        else:
            #添加到我的任务
            user.tasks_accepted.add(task)
            msg = {'msg': 'ok'}
    else:
        msg = {'msg': 'you had already accepted it'}
    return JsonResponse(msg)

@login_required
def wechatUserTaskAccepted(request):
    """
    用户接受的任务
    """
    user = request.user
    userAcTaskList = list(user.tasks_accepted.all().values(
        'task_inc_id',
        'task_tag',
        'task_owner__username',
        'task_description',
        'task_data_num',
        'task_credits',
        'task_deadline',
        'task_onelevel_type__data_type_name',
        'task_twolevel_type__data_2ltype_name',
        'task_create_datetime'
    ))
    return JsonResponse({'userAcTaskList': userAcTaskList})

@login_required
def wechatUserTaskReleased(request):
    """
    已发布的任务
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('错误请求')
    user = request.user
    userReTaskList = list(user.taskrelease_set.all().values(
        'task_inc_id',
        'task_tag',
        'task_owner__username',
        'task_description',
        'task_data_num',
        'task_credits',
        'task_deadline',
        'task_onelevel_type__data_type_name',
        'task_twolevel_type__data_2ltype_name',
        'task_create_datetime'
    ))
    return JsonResponse({'userReTaskList': userReTaskList})

@login_required
def wechatUserTaskReleasing(request):
    """
    发布新任务
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('错误请求')
    taskReleaseForm = TaskReleaseForm(request.POST)
    if taskReleaseForm.is_valid():
        newAssignment = taskReleaseForm.save()
        newAssignment.task_owner = request.user
        newAssignment.task_finish_state = "collecting"
        newAssignment.save()
        msg = {'msg': 'ok'}
    else:
        msg = {'msg': 'task wrong'}
    return JsonResponse(msg)    