#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Lib imports, they are important to help Django
a have all tools for a good use"""

# Import lib
from paypal.standard.forms import PayPalPaymentsForm

# Import Django
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# Import file
from search.forms import AnnounceForm
from user.payment_done import rent_validation_done


@csrf_exempt
def payment_done(request):
    """This is confirmation that the payment with Paypal
    is done"""
    context = {}
    rent_validation_done(request)
    context['form_announce'] = AnnounceForm()
    return render(request, 'payment/payment_done.html', context)


@csrf_exempt
def payment_canceled(request):
    """This is confirmation that the payment with Paypal
    is canceled"""
    context = {}
    context['form_announce'] = AnnounceForm()
    return render(request, 'payment/payment_canceled.html', context)


def payment_process(request, info, email_paypal, amount):
    """This is procees to payment with Paypal"""
    paypal_dict = {
        "business": email_paypal,
        "amount": amount,
        "item_name": info.title,
        "invoice": info.email,
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return":
            request.build_absolute_uri(reverse('payment_canceled')),
        "custom": "premium_plan",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {}
    context['form'] = form
    context['form_announce'] = AnnounceForm()
    return render(request, "payment/payment.html", context)
