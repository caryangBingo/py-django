# -*- coding: utf-8 -*-
# @Author: caryangBingo
# @Date:   2016-10-18 20:45:52
# @Last Modified by:   caryangBingo
# @Last Modified time: 2016-10-18 22:39:54
"""
WSGI config for guest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guest.settings")

application = get_wsgi_application()
