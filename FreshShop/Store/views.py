from django.shortcuts import render
import hashlib

# Create your views here.

# 密码加密功能
def hashpassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()