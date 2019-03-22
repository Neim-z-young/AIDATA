from .models import AppUniqueUser
class WechatOpenidAuthBackend(object):
    def get_user(self, user_id):
        try:
            return AppUniqueUser.objects.get(pk=user_id)
        except AppUniqueUser.DoesNotExist:
            return None

    def authenticate(self, request, openid):
        if openid is None:
            return None
        try:
            return AppUniqueUser.objects.get(wechat_open_id=openid)
        except AppUniqueUser.DoesNotExist:
            #创建新用户
            #创建新用户,已设置None为插入空,而不是空字符串
            return AppUniqueUser.objects.create_user(openid=openid, email=None)

class UseremailAndPasswordAuthBackend(object):
    def get_user(self, user_id=None):
        try:
            return AppUniqueUser.objects.get(pk=user_id)
        except AppUniqueUser.DoesNotExist:
            return None

    def authenticate(self, request, email=None, password=None):
        if email is None:
            return None
        try:
            user = AppUniqueUser.objects.get(email=email)
            #print(user.password)
        except AppUniqueUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
