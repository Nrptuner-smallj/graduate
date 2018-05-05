import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout

from .forms import RegisterForm,LoginForm
from .models import UserProfile, EmailCode
from utils.emailsend import send_email


# Create your views here.

class RegisterView(View):
    """注册界面的处理"""

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            nickname = request.POST.get('nickname')

            if UserProfile.objects.filter(email=email) or UserProfile.objects.filter(nickname=nickname):
                return render(request, 'register.html', dict(msg='用户名或邮箱已存在'))

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password2 != password1:
                return render(request, 'register.html', dict(msg='密码输入不一致'))

            code = request.POST.get('code')
            if not EmailCode.objects.filter(email=email, code=code, send_type="register"):
                return render(request, 'register.html', dict(msg='验证码不对'))
            user = UserProfile()
            user.email = email
            user.nickname = nickname
            user.is_active = 1
            user.password = make_password(password1)
            user.username = nickname
            user.save()
            return render(request, 'login.html')

        else:
            return render(request, 'register.html', dict(register_form=register_form))


class CustomBackend(ModelBackend):
    """自定义登录验证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 检查密码
                return user
        except Exception:
            return None


class LoginView(View):
    """登录逻辑"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return render(request,'index.html')
            else:
                return render(request,'login.html',dict(msg="用户或密码错误"))

        else:
            return render(request,'login.html',dict(login_form=login_form))


class LogoutView(View):
    """登出逻辑"""
    def get(self,request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse("index"))




class GetEmailCodeView(View):

    def post(self, request):
        email = request.POST.get("email")
        type = request.POST.get("type")
        try:
            send_email(email, type)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        except:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
