#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the some urls of the platform for user app"""

# Import Django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

# Import file
from . import views

urlpatterns = [
    url(r'^payment_process/$', views.payment_process, name="payment_process"),
    url(r'^payment_done/$', views.payment_done, name="payment_done"),
    url(r'^payment_canceled/$', views.payment_canceled,
        name="payment_canceled"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
