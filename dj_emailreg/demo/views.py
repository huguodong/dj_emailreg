from django.shortcuts import render
from  demo.models import *
from django.http import HttpResponse
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re
import token
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


# Create your views here.
def reg(request):
    if request.method == 'POST':
        user = User()
        user.username = "huguodong"
        user.pwd = "admin"
        user.email = "2228219874@qq.com"
        user.save()
        sendEmail('huguodong', '2228219874@qq.com')
        return HttpResponse('请登录邮件激活')
    else:
        return render(request, 'index.html')


def sendEmail(username, email):
    token = token_confirm.generate_validate_token(username)
    # message = "\n".join([u'{0},欢迎注册！'.format(username), u'请访问该链接，完成用户验证:',
    #                      '/'.join([settings.DOMAIN, 'activate', token])])
    # send_mail(u'注册用户验证信息', message, settings.EMAIL_HOST_USER, ['2228219874@qq.com'], fail_silently=False)
    # state = send_mail(u'注册用户验证信息', "你好啊",'531035580@qq.com', ['2228219874@qq.com'], fail_silently=False)
    subject = "注册用户信息验证"
    text_content = "\n".join([u'亲爱的用户,欢迎注册！', u'请访问该链接，完成用户验证:'])
    html = '/'.join([settings.DOMAIN, 'activate', token])
    html_content = text_content + '<a href="http://%s">http://%s</a>' % (html, html)
    msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [email])
    msg.content_subtype = "html"
    msg.send()


def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return HttpResponse('链接已过期')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('用户不存在，请重新注册')
    user.is_active = True
    user.save()
    return HttpResponse('注册成功')


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(b'afhwnfsalnwnfaosljfwn')

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=60):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(settings.SECRET_KEY)  # 定义为全局变量
