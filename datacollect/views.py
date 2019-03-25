from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from django.views.generic.edit import  UpdateView, CreateView, FormView

#装饰器
from django.contrib.auth.decorators import login_required


from .models import AppUniqueUser, \
        TaskRelease, DataType, DataTwolType, DataSubmitAndCheck
from .forms import TaskReleaseForm, UserRegisterForm, UserLoginForm, \
        DataSubmitForm, DataCheckForm, DataTypeAddForm, DataTwolTypeAddForm

# Create your views here.


def index(request):
    """
    主界面
    """
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse('datacollect:userInterface'))
    #测试cookie是否可用
    #request.session.set_test_cookie()
    userForm = UserLoginForm()
    context = {
                'userForm' : userForm,
                }
    return render(request, 'datacollect/index.html', context)

def userRegister(request):
    """
    用户注册界面
    """
    context = {}
    userRegisterForm = UserRegisterForm()
    if request.method == 'POST':
        userRegisterForm = UserRegisterForm(request.POST)
        if userRegisterForm.is_valid():
            password = userRegisterForm.cleaned_data['password']
            confirmPassword = userRegisterForm.cleaned_data['confirmPassword']
            if password == confirmPassword:
                username = userRegisterForm.cleaned_data['username']
                email = userRegisterForm.cleaned_data['email']
                try:
                    user = AppUniqueUser.objects.create_user(
                        openid=None,
                        username=username,
                        email=email,
                        password=password
                    )
                except IntegrityError:
                    context['error_message'] = '用户已存在'
                else:
                    #user.save()
                    return HttpResponseRedirect(reverse('datacollect:userRegisterProcess'))
            else:
                context['error_message'] = '前后密码不一致,请重试'
    context['userRegisterForm'] = userRegisterForm
    return render(request, 'datacollect/userRegister.html', context)

def userRegisterProcess(request):
    return render(request, 'datacollect/userRegisterProcess.html', {})

def userLogin(request):
    """
    登录界面,登录界面应该能整合到主界面下的一个标签中
    """
    context = {}
    if request.method == 'POST':
        userForm = UserLoginForm(request.POST)
        if userForm.is_valid():
            userEmail = userForm.cleaned_data['userEmail']
            password = userForm.cleaned_data['userPassword']
            user = authenticate(request, email=userEmail, password=password)
            if user is None:
                context['error_message'] = "This user doesn't exist or is invalid or password is wrong!!"
            else:
                if not request.user.is_anonymous:
                    #已有用户登录网站
                    context = {
                                'error_message': '已有用户登录网站, 请先登出原用户',
                                'userForm': userForm,
                                }
                    return render(request, 'datacollect/index.html', context)
                else:
                    user.last_login_datetime = timezone.now()
                    user.save()
                    #cookie有效则删除, 无效则请求设置
                    #print('userLog'+request.session.session_key)
                    #if not request.session.test_cookie_worked():
                    #    return HttpResponse("Please enable cookies and try again.")
                    #request.session.delete_test_cookie()
                    login(request, user)
                    return HttpResponseRedirect(reverse('datacollect:userInterface'))
    else:
        userForm = UserLoginForm()
    context['userForm'] = userForm
    return render(request, 'datacollect/index.html', context)

@login_required(login_url='datacollect:index')
def userLogout(request):
    """
    用户登出
    """
    logout(request)
    userForm = UserLoginForm()
    context = {
        'userForm': userForm,
        'error_message': '用户已登出',
    }
    return render(request, 'datacollect/index.html', context)

@login_required(login_url='datacollect:index')
def userInterface(request):
    """
    用户界面
    """
    user = request.user
    context = {
        'user': user,
    }
    #HASH_SESSION_KEY = '_auth_user_hash'
    #print(request.session[HASH_SESSION_KEY])
    #print('userFace'+request.session.session_key)
    return render(request, 'datacollect/userInterface.html', context)


#添加可发布任务的权限或会员制


##以下四个视图函数以用户-名词-动作命名,状态分为完成和进行

@login_required(login_url='datacollect:index')
def userTaskAccepted(request):
    """
    已接受的任务
    """
    user = request.user
    userAcTaskSet = user.tasks_accepted.all()
    context = {
        'userAcTaskSet': userAcTaskSet,
        }
    return render(request, 'datacollect/userTaskAccepted.html', context)

@login_required(login_url='datacollect:index')
def userTaskAccepting(request):
    """
    接受新任务
    """
    user = request.user
    pk_values = user.tasks_accepted.values_list('pk', flat=True)
    #连接查询,效率较低,可以优化
    userNAcTaskSet = TaskRelease.objects.all().exclude(pk__in=list(pk_values)).exclude(task_owner=user)
    context = {
        'userNAcTaskSet': userNAcTaskSet,
        }
    return render(request, 'datacollect/userTaskAccepting.html', context)

@login_required(login_url='datacollect:index')
def taskAcProcess(request, taskId):
    """
    接受任务后进行处理并跳转
    """
    user = request.user
    task = user.tasks_accepted.all().filter(pk=taskId)
    context={}
    if task.count() ==0:
        task = get_object_or_404(TaskRelease, pk=taskId)
        #添加到我的任务
        user.tasks_accepted.add(task)
    else:
        context['error_messages'] = 'task is already in my accepted task set'
    context['task'] = task
    return render(request, 'datacollect/taskAcProcess.html', context)

@login_required(login_url='datacollect:index')
def userTaskReleased(request):
    """
    已发布的任务
    """
    user = request.user
    userReTaskSet = user.taskrelease_set.all()
    context = {
        'userReTaskSet': userReTaskSet,
        }
    return render(request, 'datacollect/userTaskReleased.html', context)

@login_required(login_url='datacollect:index')
def userTaskReleasing(request):
    """
    发布新任务
    """
    context={}
    taskReleaseForm = TaskReleaseForm()
    if request.method=='POST':
        taskReleaseForm = TaskReleaseForm(request.POST)
        if taskReleaseForm.is_valid():
            newAssignment = taskReleaseForm.save()
            newAssignment.task_owner = request.user
            newAssignment.task_finish_state = "collecting"
            newAssignment.save()
            context = {
                'error_message': "successed",
                'assignmentname': newAssignment.task_tag,
            }
            #success url
            return render(request, 'datacollect/taskSubmit.html', context)
    context['taskReleaseForm'] = taskReleaseForm
    return render(request, 'datacollect/userTaskReleasing.html', context)

@login_required(login_url='datacollect:index')
def ajaxGetDatatype(request):
    """
    ajax异步处理下拉框, 用于发布任务时的数据类型选择
    """
    if request.method == 'GET':
        data_1l = list(DataType.objects.all().values("data_type_id", "data_type_name"))
        return JsonResponse(data_1l, safe=False)

@login_required(login_url='datacollect:index')
def ajaxChangeDatatype(request):
    """
    ajax异步处理下拉框, 用于发布任务时的数据类型选择
    """
    if request.method == 'GET':
        data_1l_id = request.GET['datatype_id']
        data_2l = list(DataTwolType.objects.filter(belongto_data_type=data_1l_id).values("data_2ltype_id", "data_2ltype_name"))
        if(data_2l == []):
            data_2l_type = DataTwolType.objects.get(pk=1)
            data_2l = [{"data_2ltype_id" : data_2l_type.data_2ltype_id,
                    "data_2ltype_name" : data_2l_type.data_2ltype_name}]
        return JsonResponse(data_2l, safe=False)

@login_required(login_url='datacollect:index')
def addTaskData(request, taskId):
    """
    给任务添加数据并进行处理
    """
    context = {}
    task = get_object_or_404(TaskRelease, pk=taskId)
    context['task'] = task
    if request.method =='POST':    
        dataSubmitForm = DataSubmitForm(request.POST, request.FILES)
        files = request.FILES.getlist('temp_data_file')
        if dataSubmitForm.is_valid():
            data_description  = dataSubmitForm.cleaned_data['data_description']
            for f in files:
                #Do something
                tempDataSubmit = DataSubmitAndCheck(
                    temp_data_file=f,
                    data_owner=request.user,
                    data_task=task,
                    data_description=data_description,
                    data_submit_datetime=timezone.now(),
                    data_check_state='checking'
                    )
                tempDataSubmit.save()
            return HttpResponseRedirect(reverse('datacollect:dataSubmitProcess'))
        else:
            context['dataSubmitForm'] = dataSubmitForm
            context['error_message'] = "form is invalid!!"
            return render(request, 'datacollect/addTaskData.html', context)
    else:
        dataSubmitForm = DataSubmitForm()
        context['dataSubmitForm'] = dataSubmitForm
        return render(request, 'datacollect/addTaskData.html', context)

@login_required(login_url='datacollect:index')
def dataSubmitProcess(request):
    """
    数据处理后给出结果
    """
    return render(request, 'datacollect/dataSubmitProcess.html', {})

@login_required(login_url='')
def taskDataList(request, taskId):
    """
    某个特定任务的数据列表
    """
    context={}
    task = get_object_or_404(TaskRelease, pk=taskId)
    dataSet = DataSubmitAndCheck.objects.filter(data_task=task).filter(data_check_state='checking')
    context['task'] = task
    context['dataSet'] = dataSet
    return render(
        request,
        'datacollect/taskDataList.html',
        context=context
    )

class DataCheckUpdateView(UpdateView):
    """
    数据审核更新视图
    """
    model = DataSubmitAndCheck
    form_class = DataCheckForm
    context_object_name = 'dataCheck'
    template_name = "datacollect/dataCheckUpdate.html"

    def get_success_url(self):
        return reverse_lazy('datacollect:dataCheckProcess', 
                args=str(self.get_object().data_task.task_inc_id))

    @login_required(login_url='datacollect:index')
    def post(self, request, *args, **kwargs):
        data = self.get_object()
        dataCheckForm = DataCheckForm(request.POST, instance=data)
        if dataCheckForm.is_valid():
            dataCheckForm.save()
            return self.form_valid(dataCheckForm)
        else:
            return self.form_invalid(dataCheckForm)

@login_required(login_url='datacollect:index')
def dataCheckProcess(request, taskId):
    """
    数据审核完成的处理结果
    """
    return render(request, 'datacollect/dataCheckProcess.html', {'taskId': taskId })

#管理员添加数据类型
@login_required(login_url='datacollect:index')
def adminAddDataType(request):
    context = {}
    dataTypeAddForm = DataTypeAddForm()
    if request.method == 'POST':
        dataTypeAddForm = DataTypeAddForm(request.POST)
        if dataTypeAddForm.is_valid():
            new_type = dataTypeAddForm.save()
            new_type.data_type_owner = request.user
            context['error_message'] = "successed"
            new_type.save()
            return HttpResponseRedirect(reverse('datacollect:userInterface'))
    context['dataTypeAddForm'] = dataTypeAddForm
    return render(request, 'datacollect/adminAddDataType.html', context)

class AdminAddDataType(CreateView):
    model = DataType
    form_class = DataTypeAddForm
    template_name = 'datacollect/adminAddDataType.html'
    success_url = reverse_lazy('datacollect:userInterface')

    @login_required(login_url='datacollect:index')
    def post(self, request, *args, **kwargs):
        dataTypeAddForm = DataTypeAddForm(request.POST)
        if dataTypeAddForm.is_valid():
            name=dataTypeAddForm.cleaned_data['data_type_name']
            description=dataTypeAddForm.cleaned_data['data_type_description']
            try:
                new_type = DataType(
                    data_type_owner=request.user,
                    data_type_name=name,
                    data_type_description=description
                )
            except IntegrityError:
                return self.form_invalid(dataTypeAddForm)
            else:
                new_type.save()
            return self.form_valid(dataTypeAddForm)
        else:
            return self.form_invalid(dataTypeAddForm)

@login_required(login_url='datacollect:index')
def adminAddDataTwolType(request):
    context = {}
    dataTwolTypeAddForm = DataTwolTypeAddForm()
    if request.method == 'POST':
        dataTwolTypeAddForm = DataTwolTypeAddForm(request.POST)
        if dataTwolTypeAddForm.is_valid():
            new_type = dataTwolTypeAddForm.save()
            new_type.data_2ltype_owner = request.user
            context['error_message'] = "successed"
            new_type.save()
            return HttpResponseRedirect(reverse('datacollect:userInterface'))
    context['dataTwolTypeAddForm'] = dataTwolTypeAddForm
    return render(request, 'datacollect/adminAddDataTwolType.html', context)
