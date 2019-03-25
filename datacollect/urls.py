from django.urls import path

from . import views, weChatViews

app_name = 'datacollect'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/user/', views.userRegister, name='userRegister'),
    path('registered/user/', views.userRegisterProcess, name='userRegisterProcess'),
    path('login/user/', views.userLogin, name='userLogin'),
    path('logout/user/', views.userLogout, name='userLogout'),
    path('userInterface/', views.userInterface, name='userInterface'),
    path('userTaskAccepted/',views.userTaskAccepted, name='userTaskAccepted'),
    path('userTaskAccepting/', views.userTaskAccepting, name='userTaskAccepting'),
    path('taskAcProcess/<int:taskId>/', views.taskAcProcess, name='taskAcProcess'),
    path('userTaskReleased/', views.userTaskReleased, name='userTaskReleased'),
    path('userTaskReleasing/', views.userTaskReleasing, name='userTaskReleasing'),
    path('admin/ajaxChangeDatatype/', views.ajaxChangeDatatype, name='ajaxChangeDatatype'),
    path('admin/ajaxGetDatatype/', views.ajaxGetDatatype, name='ajaxGetDatatype'),
    path('user/addTaskData/<int:taskId>/', views.addTaskData, name='addTaskData'),
    path('user/dataSubmitProcess/',views.dataSubmitProcess, name='dataSubmitProcess'),
    path('user/<int:taskId>/taskDataList/', views.taskDataList, name='taskDataList'),
    path('user/dataCheckUpdate/<int:pk>/', views.DataCheckUpdateView.as_view(), name='dataCheckUpdate'),
    path('user/<int:taskId>/dataCheckProcess/', views.dataCheckProcess, name='dataCheckProcess'),
    #管理员
    path('admin/adminAddDataType/', views.adminAddDataType, name='adminAddDataType'),
    path('admin/adminAddDataTwolType/', views.adminAddDataTwolType, name='adminAddDataTwolType'),
    #微信小程序视图
    path('wechat/user/login/', weChatViews.wechatLogin),
    path('wechat/taskList/', weChatViews.wechatTaskList),
    path('wechat/tackAccepting/', weChatViews.wechatUserTaskAccepting),
    path('wechat/taskAccepted/', weChatViews.wechatUserTaskAccepted),
    path('wechat/taskReleased/', weChatViews.wechatUserTaskReleased),
    path('wechat/taskReleasing/', weChatViews.wechatUserTaskReleasing),
]
