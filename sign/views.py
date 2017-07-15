# -*- coding: utf-8 -*-
# @Author: Caryang
# @Date:   2016-10-12 22:52:34
# @Last Modified by:   caryangBingo
# @Last Modified time: 2017-07-16 00:25:11
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
	paginator = Paginator(guest_list, 2)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		#if page is not an integer,deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
		#if page is out of range(e.g. 9999),deliver last page of results.
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

"""
@login_required
def search_name(request):
	username = request.session.get('user','')
	if 'search_name' in request.GET.get:
		search_name = request.GET['search_name']
		if not search_name:
			return render(request,'index.html')
		else:
			event_list = Event.objects.filter(name__contains=search_name)
			if len(event_list) == 0:
				return render(request,'event_manage.html',{'events':event_list,"error":True})
			else:
				return render(request,'event_manage.html',{'events':event_list,"error":False})
	return redirect("")
"""

@login_required
def search_name(request):
	username = request.session.get('user','')
	search_name = request.GET.get("name","")
	event_list = Event.objects.filter(name__contains=search_name)
	return render(request,"event_manage.html",{"user": username,
																					"events": event_list})

#嘉宾列表手机号搜索
@login_required
def search_phone(request):
	username = request.session.get('user','')
	search_phone = request.GET.get("phone","")
	#print(search_phone)
	#search_phone_bytes = search_phone.encode(encoding="utf-8")
	guest_list = Event.objects.filter(name__contains=search_phone)
	return render(request,"guest_manage.html",{"user":username,																					"guests": guest_list})


#签到页面
@login_required
def sign_index(request,eid):
	event = get_object_or_404(Event,id=eid)
	return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,eid):
	event = get_object_or_404(Event, id=eid)
	phone = request.POST.get('phone','')
	print(phone)

	result = Guest.objects.filter(phone=phone)
	if not result:
		return render(request,'sign_index.html',{'event': event,'hint': 'phone error.'})

	result = Guest.objects.filter(phone=phone,event_id=eid)
	if not result:
		return render(request,'sign_index.html',{'event': event,'hint': 'event id or phone error.'})

	result = Guest.objects.get(phone=phone,event_id=eid)
	if result.sign:
		return render(request,'sign_index.html',{'event': event,'hint': "user has sign in."})
	else:
		Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
		return render(request,'sign_index.html',{'event': event,'hint': 'sign in success!','guest': result})


#退出登录
@login_required
def logout(request):
	auth.logout(request)
	response = HttpResponseRedirect('/')
	return response
