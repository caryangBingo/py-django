# -*- coding: utf-8 -*-
# @Author: crazyang
# @Date:   2016-10-13 11:02:13
# @Last Modified by:   crazyang
# @Last Modified time: 2016-10-24 16:52:58
from django.test import TestCase
from sign.models import Event,Guest

# Create your tests here.
class ModelTest(TestCase):
	def setUp(self):
		Event.objects.create(id=1,name="oneplus 3 event",status=True,limit=2000,address='shenzhen',start_time='2016-08-31')
