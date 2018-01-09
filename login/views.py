# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import transaction
from django.http import JsonResponse

from . import forms
import models
# Create your views here.


def index(request):
    # pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html')


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def game(request,game_id = None,channel = None):
    if request.method == 'POST':
        try:
            keys = request.POST.keys()
            print keys
            with transaction.atomic():
                game = models.Game.objects.create(game_id = int(request.POST['game_id']))
                for key in keys:
                    if key != 'game_id':
                        game.__dict__[key] = request.POST[key]
                game.save()
            return JsonResponse({'code':0,'msg':u'操作成功'})
        except Exception as e:
            return JsonResponse({'code':-1,'msg':str(e)})
    else:
        if game_id == None and channel == None:
            context = {}
            all_entries = models.Game.objects.all()[:20]
            data = []
            for item in all_entries:
                value = []
                value.append(item.game_id)
                value.append(item.game_name)
                value.append(item.url_update)
                value.append(item.game_server)
                value.append(item.game_desc)
                data.append(value)
            context['items'] = data
            return render(request, 'game/game.html',context)
        elif game_id != None and channel == None:
            return HttpResponse("game")
        elif game_id != None and channel != None:
            return HttpResponse("channel")

# 添加白名单
def whiteList(request):
    context = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                uuid = request.POST['uuid']
                inst = None
                try:
                    inst = models.WhiteList.objects.get(uuid=uuid)
                except:
                    inst = models.WhiteList.objects.create(uuid=uuid)
                inst.name = request.POST['name']
                inst.platform = request.POST['platform']
                inst.save()
            return JsonResponse({'code': 0, 'msg': u'操作成功'})
        except Exception as e:
            return JsonResponse({'code': -1, 'msg': str(e)})
    else:
        context = {}
        all_entries = models.WhiteList.objects.all()[:20]
        data = []
        for item in all_entries:
            value = []
            value.append(item.uuid)
            value.append(item.name)
            value.append(item.platform)
            data.append(value)
        context['items'] = data
        return render(request, 'game/white.html',context)

# 添加模块
def versionCtrl(request):
    return render(request,"game/version.html")
