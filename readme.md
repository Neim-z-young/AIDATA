#### AI数据采集项目

文件目录树
```python
.
│  .gitignore
│  docker-compose.yml             #docker配置
│  manage.py
│  readme.md
│  微信小程序接口说明.txt
│
├─.vscode
│      settings.json
│
├─AIdatacollect
│      AIdatacollect_nginx.conf    #nginx配置
│      AIdatacollect_uwsgi.ini     #uwsgi配置
│      settings.py                 #项目设置
│      urls.py                     #项目路由配置
│      uwsgi_params                #uwsgi参数
│      wsgi.py
│      __init__.py
│
└─datacollect                      #项目应用
    │  admin.py
    │  apps.py
    │  customAuth.py               #自定义管理员
    │  customUser.py               #自定义用户
    │  forms.py                    #定义表单类
    │  models.py                   #模型定义
    │  tests.py
    │  urls.py                     #定义URL路由规则
    │  views.py                    #定义网页视图
    │  weChatViews.py              #定义微信接口
    │  __init__.py
    │
    └─templates
        └─datacollect              #数据采集项目网页
                addTaskData.html
                adminAddDataTwolType.html
                adminAddDataType.html
                dataCheckProcess.html
                dataCheckUpdate.html
                dataSubmitProcess.html
                index.html
                taskAcProcess.html
                taskDataList.html
                taskSubmit.html
                userInterface.html
                userRegister.html
                userRegisterProcess.html
                userTaskAccepted.html
                userTaskAccepting.html
                userTaskReleased.html
                userTaskReleasing.html
```