# -*- coding: utf-8 -*-
# @Author: Caryang
# @Date:   2016-10-12 22:52:34
# @Last Modified by:   Caryang
# @Last Modified time: 2016-10-16 16:05:54
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event

# Create your views here.
#def index(request):
#	return HttpResponse("Hello Django!!!")

def index(request):
	return render(request,"index.html")

#登录动作
'''
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		if username == 'admin' and password == '1234admin':
			response = HttpResponseRedirect('/event_manage/')
			request.session['user'] = username
			return response
		else:
			return render(request,'index.html',{'error':'username or password error!'})
'''
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			request.session['user'] = username
			response = HttpResponseRedirect('/event_manage/')
			return response
		else:
			return render(request, 'index.html', {'erros':'username or password error'})

#发布会管理
#
@login_required

#def event_manage(request):
#	username = request.session.get('user','')
#	return render(request,"event_manage.html",{"user":username})

def event_manage(request):
	event_list = Event.objects.all()
	username = request.session.get('user','')
	return render(request,"event_manage.html",{"user":username,"events":event_list})

#发布会名称搜索
@login_required
def sreach_name(request):
	username = request.session.get('user','')
	sreach_name = request.GET.get("name","")
	sreach_name_bytes = sreach_name.encode(encoding="utf-8")
	event_list = Event.objects.filter(name_contains=sreach_name)
	return render(request,"event_manage.html",{"user":username,"events":event_list})