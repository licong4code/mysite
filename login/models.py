# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Game(models.Model):
    game_id = models.IntegerField(unique=True)
    game_name = models.CharField(max_length=512,verbose_name=u'游戏名称')
    url_update = models.CharField(max_length=512,verbose_name=u'更新地址',default='')
    game_server = models.CharField(max_length=512,verbose_name=u'服务器地址')
    game_desc = models.TextField()

# 白名单
class WhiteList(models.Model):
    name = models.CharField(max_length=512, verbose_name=u'玩家名称')
    uuid = models.CharField(max_length=512, verbose_name=u'设备标识码')
    platform = models.CharField(max_length=128, verbose_name=u'平台')

class Version(models.Model):
    name = models.CharField(unique=True,max_length=128,verbose_name=u'模块名称')
    debug_version = models.IntegerField()
    release_version = models.IntegerField()


