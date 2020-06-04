#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the some urls of the platform for user app"""

# Import Django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include

# Import file
from . import views

urlpatterns = [
    url(r'^connect.html', views.connect, name="connect"),
    url(r'^sign_up.html', views.sign_up, name="sign_up"),
    url(r'^gcu.html', views.gcu, name="gcu"),
    url(r'^dashboard.html', views.dashboard, name="dashboard"),
    url(r'^disconnect.html', views.disconnect, name="disconnect"),

    #  Password reset URL
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name="password_reset"),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    # Booking URL
    url(r'^rent_now.html', views.rent_now, name="rent_now"),
    url(r'^rent_validation.html', views.rent_validation,
        name="rent_validation"),
    url(r'^user_booking_info.html', views.user_booking_info,
        name="user_booking_info"),
    url(r'^new_ad.html', views.new_ad, name="new_ad"),
    url(r'^handler_ad.html', views.handler_ad, name="handler_ad"),
    url(r'^rented.html', views.rented, name="rented"),

    # Booking canceled URL
    url(r'^cancel_rented.html', views.cancel_rented,
        name="cancel_rented"),
    url(r'^cancel_validation.html', views.cancel_myrented,
        name="cancel_validation"),
    url(r'^delete_rent.html', views.delete_rent_available,
        name="delete_rent"),
    url(r'^delete_validation.html', views.delete_my_offer,
        name="delete_validation"),

    # Change announces
    url(r'^change_pics.html', views.change_pics,
        name="change_pics"),
    url(r'^change_price.html', views.change_price,
        name="change_price"),

    # Paypal URL
    url(r'^add_email_paypal.html', views.add_email_paypal,
        name="add_email_paypal"),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include('payment.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
