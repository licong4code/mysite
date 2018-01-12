# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import transaction
from django.http import JsonResponse
import MySQLdb

from django.shortcuts import render
from share import factory
import json,base64
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
KEY = 'UEK9B4QejJqCAYhw'

# Create your views here.
share_img_factory = None
red_db = None
red_cursor = None

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)


def share(request):
    try:
        global share_img_factory
        if share_img_factory == None:
            share_img_factory = factory.Creator()
        data = json.loads(decode_base64(request.GET["data"]))
        if data["type"] == 1:
            def conndb():
                global red_db
                global red_cursor
                red_db = MySQLdb.connect(host="xxx.79.2.xxx", port=0, user='', passwd='', db='',charset='utf8')
                red_cursor = red_db.cursor()

            try:
                if red_db == None:
                    conndb()
                else:
                    red_db.ping()
            except Exception as e:
                conndb()

            sql = 'SELECT amount FROM bjd_red_packet_tools WHERE account="{0}"'.format(data['account'])
            result = red_cursor.execute(sql)
            if result >  0:
                data["total"] = red_cursor.fetchone()[0]

        url = "http://update.pukegame.com/download/" + share_img_factory.build(data)
        return JsonResponse({"code": 0,"url":url})
        # else:
        #     return JsonResponse({"code": -1, "msg": u'非法请求'})
    except Exception, e:
        return JsonResponse({"code": - 1,"msg":str(e)})