#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file is a file to cut an import circular
This import is mandatory for the good of the system"""

# Import Django
from django.core.mail import send_mail
from django.shortcuts import render

# Import file
from search.forms import AnnounceForm
from .models import User, MyRental, Booking, Announces

# This list is there to obtain information for the reservation
list_info_rent = []


def get_info_booking(request, announce, d_min, d_max):
    """This method gives the information to the above list"""
    for info in announce:
        list_info_rent.append(info.city)
        list_info_rent.append(info.country)
        list_info_rent.append(info.code)
        list_info_rent.append(info.email)
        list_info_rent.append(info.title)
        list_info_rent.append(d_min)
        list_info_rent.append(d_max)


def rent_validation_done(request):
    """Rent_validation is there to confirm the rental by email
    and save the booking"""
    context = {}
    user = User.objects.get(id=request.session['member_id'])

    if len(list_info_rent) == 0:
        context['error_rent_validation'] = \
            "Veuillez nous excuser une erreur c'est produite. \n " \
            "Nous vous conseillons de réessayer ultérieurement."
        context['form_announce'] = AnnounceForm()
        return render(request, 'search/rent_now.html', context)
    else:
        email_validation_customer(request, user)
        email_validation_trader(request, list_info_rent[3],
                                list_info_rent[4])

        new_rental = MyRental(
            user=user,
            rental_city=list_info_rent[0],
            rental_country=list_info_rent[1],
            email_user_rental=user.email,
            code=list_info_rent[2]
        )
        new_rental.save()

        new_booking = Booking(
            user=user,
            code=list_info_rent[2],
            date_min=list_info_rent[5],
            date_max=list_info_rent[6]
        )
        update_announce = Announces.objects.get(code=list_info_rent[2])
        update_announce.booking = "Votre bien est actuellement loué."

        update_announce.save()
        new_booking.save()
        context['form_announce'] = AnnounceForm()


def email_validation_customer(request, user):
    """Validation by e-mail is the method to send an e-mail
    to a customer or a merchant to report that a property is rented"""
    send_mail(
        'Location - ImmoLocation',
        'Bonjour,\n'
        'Heureux de vous avoir parmis nos utilisateurs, '
        'nous vous en remercions. \n'
        'Nous sommes également dans le plaisir de vous annoncer '
        'que la location a bien été validé. \n'
        'Merci. \n'
        'Cordialement, \n',
        'Immolocation@outlook.fr',
        [user.email],
        fail_silently=False,
    )


def email_validation_trader(request, email, title):
    """Validation by e-mail is the method to send an e-mail
    to a customer or a merchant to report that a property is rented"""
    send_mail(
        'Location - ImmoLocation',
        'Bonjour,\n'
        'Heureux de vous avoir parmis nos utilisateurs, '
        'nous vous en remercions. \n'
        'Nous sommes également dans le plaisir de vous annoncer '
        'que votre bien ' + title + 'a été loué. \n'
        'Merci. \n'
        'Cordialement, \n',
        'Immolocation@outlook.fr',
        [email],
        fail_silently=False,
    )
