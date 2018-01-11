# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import transaction
from django.http import JsonResponse

from django.shortcuts import render
from share import factory
# Create your views here.

#
def share(request):
    try:
        filename = factory.run([{"text":u" 获得 ","color":(18,10,10)},{"text":u"1.88","color":(255,0,0)},{"text":u' 微信红包',"color":(18,10,10)}])
        url = "http://update.pukegame.com/download/" + filename
        return JsonResponse({"code": 0,"url":url})
    except Exception, e:
        return JsonResponse({"code": - 1,"msg":str(e)})