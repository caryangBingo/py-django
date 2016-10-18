# -*- coding: utf-8 -*-
# @Author: caryangBingo
# @Date:   2016-10-18 20:45:52
# @Last Modified by:   caryangBingo
# @Last Modified time: 2016-10-18 22:39:25
from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.
class EventAdmin(admin.ModelAdmin):
	list_display = ['name','status','start_time','id']
	search_fields = ['name']
	list_filter = ['status']

class GuestAdmin(admin.ModelAdmin):
	list_display = ['realname','phone','email','sign','create_time','event']
	search_fields = ['realname','phone']
	list_filter = ['sign']

admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)
