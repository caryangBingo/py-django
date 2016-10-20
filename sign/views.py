# -*- coding: utf-8 -*-
# @Author: Caryang
# @Date:   2016-10-12 22:52:34
# @Last Modified by:   crazyang
# @Last Modified time: 2016-10-20 18:26:36
from django.shortcuts import render
from django.contrib import auth
from sign.models import Event,Guest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404

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
#def event_manage(request):
#	username = request.session.get('user','')
#	return render(request,"event_manage.html",{"user":username})

@login_required
def event_manage(request):
	event_list = Event.objects.all()
	username = request.session.get('user','')
	return render(request,"event_manage.html",{"user":username,"events":event_list})

#嘉宾管理
"""
@login_required
def guest_manage(request):
	guest_list = Guest.objects.all()
	username = request.session.get('user','')
	return render(request,"guest_manage.html",{"user":username,"guests":guest_list})
"""

@login_required
def guest_manage(request):
	username = request.session.get('user','')
	guest_list = Guest.objects.all()
	paginator = Paginator(guest_list,2)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		#if page is not an integer,deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
		#if page is out of range(e.g.9999),deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	return render(request,"guest_manage.html",{"user":username,"guests":contacts})

#发布会名称搜索
"""
@login_required
def sreach_name(request):
	username = request.session.get('user','')
	sreach_name = request.GET.get('name','')
	#sreach_name_bytes = sreach_name.encode(encoding="utf-8")
	event_list = Event.objects.filter(name__icontains=sreach_name)
	return render(request,"event_manage.html",{"user":username,"events":event_list})
"""

@login_required
def sreach_name(request):
	username = request.session.get('user','')
	if 'sreach_name' request.GET:
		sreach_name = request.GET['sreach_name']
		if not sreach_name:
			return render(request,'index.html')
		else:
			event_list = Event.objects.filter(name__icontains=sreach_name)
			if len(event_list) == 0:
				return render(request,'event_manage.html',{"events":event_list,"error":True})
			else:
				return render(request,'event_manage.html',{"events",event_list,"error":False})
	return redirect("")

#嘉宾列表手机号搜索
@login_required
def sreach_phone(request):
	username = request.session.get('user','')
	sreach_name = request.GET.get("phone","")
	#sreach_name_bytes = sreach_name.encode(encoding="utf-8")
	guest_list = Event.objects.filter(phone__contains=sreach_name)
	return render(request,"guest_manage.html",{"user":username,"events":guest_list})


#签到页面
@login_required
def sign_index(request,event_id):
	event = get_object_or_404(Event,id=event_id)
	return render(request,'sign_index.html',{'event':event})
