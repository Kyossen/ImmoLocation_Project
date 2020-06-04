#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the somes urls of the platform for search app"""

# Import Django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include

# Import file
from . import views

urlpatterns = [
    url(r'^result.html', views.result, name="result"),
    url(r'^description.html', views.description, name="description"),
    url(r'^copyright.html', views.copyright_page, name="copyright"),

    # Paypal URL
    url(r'^paypal/', include('paypal.standard.ipn.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
