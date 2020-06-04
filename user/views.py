#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Lib imports, they are important to help Django a have all tools for a good use
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning"""

# Import lib
import time
from datetime import date, datetime
from random import randrange

# Import Django
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

# Import file
from payment.views import payment_process
from search.forms import AnnounceForm
from .payment_done import get_info_booking
from .models import Announces, User, MyRental, Booking
from .forms import ConnectForm, ParagraphErrorList, \
    UserCreationForm, New_AdForm, Rent_Now


def sign_up(request):
    """Sing_up function is the function for allow a user on sign up"""
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST, error_class=ParagraphErrorList)
        # Check input if she valid or not
        if form.is_valid():
            if request.POST.get('gcu'):
                user = form.save()
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                request.session['member_id'] = user.id
                return redirect('dashboard')
            else:
                context['error'] = 'Veuillez accepter les ' \
                                   'conditions générales d\'utilisation'
                context['form'] = form
                context['form_announce'] = AnnounceForm()
                return render(request, 'user/sign_up.html',
                              context, status=401)
        else:
            context['form'] = form
            context['form_announce'] = AnnounceForm()
            return render(request, 'user/sign_up.html', context, status=401)
    else:
        # GET method. Create a new form to be used in the template.
        form = UserCreationForm()
    context['form_announce'] = AnnounceForm()
    context['form'] = form
    return render(request, 'user/sign_up.html', context)


def hasNumbers(inputString):
    """This method searches whether a string contains a number or not"""
    return any(char.isdigit() for char in inputString)


def gcu(request):
    context = {}
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/gcu.html', context)


def connect(request):
    """The connect function is the function
    allow a user of the connect on the platform"""
    context = {}
    # Check if user is connect or not
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            # Check if input is good
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('wordpass')
                return check_connect(request, email, password)

            else:
                context['errors'] = form.errors.items()
                return render(request, 'user/connect.html', context,
                              status=401)
        else:
            form = ConnectForm()
        context['form'] = form
        context['form_announce'] = AnnounceForm()
        return render(request, 'user/connect.html', context)

    # If the user clicks on the login page and the user is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard.html')


def check_connect(request, email, password):
    """Here, the system check if information
     the user is good or not
    If they are good, the system create
     a session for the user"""
    context = {}
    user_connected = authenticate(request, email=email, password=password)
    # Check if input is good or not
    if user_connected is not None:
        # create a session for user
        login(request, user=user_connected)
        request.session['member_id'] = user_connected.id
        time.sleep(4)
        return HttpResponseRedirect('dashboard.html')
    else:
        context['form'] = ConnectForm()
        context['form_announce'] = AnnounceForm()
        context['error_login'] = "Adresse email et/ou mot de passe incorrect"
        return render(request, 'user/connect.html', context, status=401)


def dashboard(request):
    """Dashboard is the handler of the user dashboard"""
    context = {}
    # Check if user is connect or not
    if not request.user.is_authenticated:
        return render(request, 'user/connect.html', context)
    else:
        # Find the user in all users
        user = request.user
        context['email'] = user.email
        context['email_paypal'] = user.email_paypal
        context['firstname'] = user.first_name
        context['lastname'] = user.last_name
        # Get all information the user
        context['phone'] = user.phone
        context['date_of_birth'] = user.date_of_birth
        context['postal_address'] = user.postal_address
        context['form_announce'] = AnnounceForm()
        return render(request, 'user/dashboard.html',
                      context)


def add_email_paypal(request):
    """This method is to add an email paypal for a user """
    context = {}
    if request.method == "POST":
        email_paypal = request.POST.get('email')
        user = User.objects.get(pk=request.session['member_id'])
        user.email_paypal = email_paypal
        user.save()
        context['form_announce'] = AnnounceForm()
        return HttpResponseRedirect('dashboard.html')
    context['form_ad'] = New_AdForm()
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/add_email_paypal.html', context)


def disconnect(request):
    """Disconnect is the method for disconnect a user"""
    context = {}
    # Check if user is connect
    if not request.user.is_authenticated:
        context['form_announce'] = AnnounceForm()
        return render(request, 'search/index.html', context)
    else:
        # If user is connect, user is disconnect and redirect to home page
        auth_logout(request)
        context['form_announce'] = AnnounceForm()
        return redirect('index')


def new_ad(request):
    """New ad is the method for save the
    new advertissements of the users"""
    context = {}
    nb_1 = randrange(0, 101, 2)
    nb_2 = randrange(0, 101, 2)

    if request.method == 'POST':
        r_title = request.POST.get('title')
        r_address = request.POST.get('address')
        r_description = request.POST.get('description')
        r_city = request.POST.get('city')
        r_country = request.POST.get('country')
        r_price_day = request.POST.get('price_day')
        r_price_weeks = request.POST.get('price_weeks')
        r_date = request.POST.get('date')
        r_email = request.POST.get('email')
        r_pics_1 = request.FILES['pics_1']
        r_pics_2 = request.FILES['pics_2']
        r_pics_3 = request.FILES['pics_3']
        math_1 = nb_1 * nb_2
        math_2 = math_1 * nb_1
        code = math_2
        if code > 0:
            pass
        else:
            nb_3 = randrange(0, 101, 2)
            code = math_2 + nb_3 - 1
        if r_price_day.isdigit() and r_price_weeks.isdigit():
            new_ad = Announces(title=r_title,
                               address=r_address,
                               description=r_description,
                               city=r_city,
                               country=r_country,
                               price_day=r_price_day,
                               price_weeks=r_price_weeks,
                               date=r_date,
                               email=r_email,
                               pics_1=r_pics_1,
                               pics_2=r_pics_2,
                               pics_3=r_pics_3,
                               code=code,
                               user_id=request.session['member_id'])
            new_ad.save()

            context['form_ad'] = New_AdForm()
            context['form_announce'] = AnnounceForm()
            return HttpResponseRedirect('dashboard.html')
        else:
            context['error_price'] = 'Veuillez indiquer un montant valide'
            context['form_ad'] = New_AdForm()
            context['form_announce'] = AnnounceForm()
            return render(request, 'search/new_ad.html', context)

    context['form_ad'] = New_AdForm()
    context['form_announce'] = AnnounceForm()
    return render(request, 'search/new_ad.html', context)


def handler_ad(request):
    """Handler_ad is the method for manage of
    the rentals"""
    context = {}
    if request.user.is_authenticated:
        announces_user = \
            Announces.objects.filter(user_id=request.session['member_id'])
        rental_all = MyRental.objects.all()
        for info in announces_user:
            for rent in rental_all:
                if info.code == rent.code:
                    user = User.objects.filter(pk=rent.user_id)
                    context['user_booking'] = user
        context['informations_announces'] = announces_user

        paginator = Paginator(announces_user, 6)
        page = request.GET.get('page', 1)
        nb_page = paginator.get_page(page)
        context['nb_page'] = nb_page
        context['informations_announces'] = paginator.page(page)
        context['form_announce'] = AnnounceForm()
        return render(request, 'user/handler_ad.html', context)
    else:
        context['error_handler'] = "Vous devez être connecté " \
                                   "pour accéder à cette page."
    context['form_ad'] = New_AdForm()
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/handler_ad.html', context)


def user_booking_info(request):
    """Here we get the user information to give it to the owner"""
    context = {}
    info_user = request.GET.get('user')
    search_user = MyRental.objects.filter(code=info_user)
    users_all = User.objects.all()
    if search_user:
        for info in search_user:
            for info_all in users_all:
                if info.user_id == info_all.pk:
                    context['first_name'] = info_all.first_name
                    context['last_name'] = info_all.last_name
                    context['email'] = info_all.email
                    context['phone'] = info_all.phone
    else:
        pass
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/user_booking_info.html', context)


def delete_rent_available(request):
    """Cancel and delete location is there to get
    cancellation information on the property"""
    context = {}
    code = request.GET.get('announce')
    code_cancel = request.GET.get('cancel')
    if request.user.is_authenticated:
        if 'cancel' in request.GET:
            announce = Announces.objects.filter(code=code_cancel)
            return delete_my_offer(request, announce)
        elif 'announce' in request.GET:
            pass
        else:
            context['error_cancel'] = 'Un problème est survenu ' \
                                      'veuillez réessayer ultérieurement.'

    else:
        context['error_cancel'] = 'Vous devez être connecté ' \
                                  'pour accéder à cette page'
    context['code'] = code
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/delete_rent.html', context)


def delete_my_offer(request, announce):
    """Canceling my offer means canceling
    and remove from the database the fact that a
    the user can rent the property"""
    context = {}
    for info in announce:
        contact_owner(request, info)
        remove_announce = Announces.objects.get(code=info.code)
        remove_announce.delete()

    context['form_announce'] = AnnounceForm()
    return render(request, 'user/delete_validation.html', context)


def rent_now(request):
    """Rent_now is there to allow rental of the ad"""
    context = {}
    # Check if announce is present in the url
    announce_id = request.GET.get('announce')
    # Filter the id of the rental for be sure that is a good rental
    announce = Announces.objects.filter(code=announce_id)
    booking = Booking.objects.filter(code=announce_id)
    for info in announce:
        context['info_pk'] = info.pk
        context['info_code'] = info.code
        if not request.user.is_authenticated:
            context['error_rent_now'] = "Vous devez être connecté" \
                                        " pour accéder à cette page."
            context['form_announce'] = AnnounceForm()
            return render(request, 'search/rent_now.html', context)
        else:
            context['informations_announces'] = announce
            context['form_ad'] = Rent_Now()
            context['form_announce'] = AnnounceForm()
            check_the_available_dates(request, booking)
            return render(request, 'search/rent_now.html', context)


def check_the_available_dates(request, booking):
    context = {}
    for info in booking:
        print(info.date_min)
        print(type(info.date_min))
        date_min_good = info.date_min.replace("-", "/")
        date_max_good = info.date_max.replace("-", "/")
        d1 = (datetime.strptime(date_min_good, "%d/%m/%Y"))
        d2 = (datetime.strptime(date_max_good, "%d/%m/%Y"))
        print('D1: ', d1)
        print('D2: ', d2)
        time_booking = str(f"{d1.day - d2.day}")
        print(time_booking)
        data = {'date_min': d1,
                'date_max': d2}
        return JsonResponse(data)


def rent_validation(request):
    """Rent_validation is there to confirm of the rental"""
    context = {}
    announce_id = request.GET.get('announce')
    # Filter the id of the rental for be sure that is a good rental
    announce = Announces.objects.filter(code=announce_id)
    if request.method == 'POST':
        # Prepare the amount for payment and check dates
        date_min = request.POST.get('date_min')
        date_max = request.POST.get('date_max')
        date_min_good = date_min.replace("-", "/")
        date_max_good = date_max.replace("-", "/")
        d1 = (datetime.strptime(date_min_good, "%d/%m/%Y"))
        d2 = (datetime.strptime(date_max_good, "%d/%m/%Y"))
        time_booking = str(f"{d1.day - d2.day}")
        correct_time = time_booking.replace("-", "")
        for info in announce:
            context['form_announce'] = AnnounceForm()
            amount = info.price_day * int(correct_time)
            user = User.objects.get(pk=info.user_id)
            get_info_booking(request, announce, date_min, date_max)
            return payment_process(request, info,
                                   user.email_paypal,
                                   amount)


def rented(request):
    """This method is used to send a message
    if the user has not rented property, or
    to continue displaying the process of
    the rented property"""
    context = {}
    rented_all = MyRental.objects.filter(
        user__id=request.user.id)
    # Check if user have already added of the rented
    if len(rented_all) != 0:
        return display_my_rented(request, rented_all)
    else:
        context['form_announce'] = AnnounceForm()
        context['not_rented'] = "Vous n'avez pas " \
                                "encore loué de bien."
        return render(request, 'user/my_rent.html', context)


def display_my_rented(request, rented_all):
    """Display_my_rented property is the method
    to display the user's rented property"""
    context = {}
    paginator = Paginator(rented_all, 6)
    page = request.GET.get('page', 1)
    nb_page = paginator.get_page(page)
    context['nb_page'] = nb_page
    context['announce_rented'] = rented_all
    context['announce_rented'] = paginator.page(page)
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/my_rent.html', context)


def cancel_rented(request):
    """Cancel rented is the method for get
    the cancel infos of the proprety"""
    context = {}
    code = request.GET.get('announce')
    code_cancel = request.GET.get('cancel')
    if request.user.is_authenticated:
        if 'cancel' in request.GET:
            announce = Announces.objects.filter(code=code_cancel)
            return cancel_myrented(request, announce)
        elif 'announce' in request.GET:
            pass
        else:
            context['error_cancel'] = 'Un problème est survenu ' \
                                      'veuillez réessayer ultérieurement.'

    else:
        context['error_cancel'] = 'Vous devez être connecté ' \
                                  'pour accéder à cette page'
    context['code'] = code
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/cancel_rented.html', context)


def cancel_myrented(request, announce):
    """Cancel my rental is to effect the cancellation
    and to delete from the database the fact that a
    user is renting the property"""
    context = {}
    for info in announce:
        contact_owner(request, info)
        remove_myrent = MyRental.objects.get(code=info.code)
        remove_myrent.delete()
        remove_booking = Booking.objects.get(code=info.code)
        remove_booking.delete()
        update_announce = Announces.objects.get(code=info.code)
        update_announce.booking = ""
        update_announce.save()

    context['form_announce'] = AnnounceForm()
    return render(request, 'user/cancel_validation.html', context)


def contact_owner(request, info):
    """Contact the owner because his property is canceled"""
    send_mail(
        'Location - ImmoLocation',
        'Bonjour,\n'
        'Je viens vous informé que votre location '
        'est de nouveau disponible. \n'
        'En effet, la location ' + info.title +
        'a été annulée. \n'
        'Merci. \n'
        'Cordialement, \n',
        'Immolocation@outlook.fr',
        [info.email],
        fail_silently=False,
    )


def change_pics(request):
    """Change pics is the method for get
    the cancel infos of the property"""
    context = {}
    code = request.GET.get('announce')
    code_change = request.GET.get('change')
    if request.user.is_authenticated:
        if 'change' in request.GET:
            announce = Announces.objects.filter(code=code_change)
            pics_1 = request.FILES['pics_1']
            pics_2 = request.FILES['pics_2']
            pics_3 = request.FILES['pics_3']
            return change_pics_validation(request, announce, pics_1,
                                          pics_2, pics_3)
        elif 'announce' in request.GET:
            pass
        else:
            context['error_cancel'] = 'Un problème est survenu ' \
                                      'veuillez réessayer ultérieurement.'

    else:
        context['error_cancel'] = 'Vous devez être connecté ' \
                                  'pour accéder à cette page'
    context['code'] = code
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/change_pics.html', context)


def change_pics_validation(request, announce, pics_1,
                           pics_2, pics_3):
    """Change pics validation confirm the validation to pics"""
    context = {}
    for info in announce:
        contact_owner(request, info)
        print(pics_1, pics_2, pics_3)
        announce_pics = Announces.objects.get(code=info.code)
        announce_pics.pics_1 = pics_1
        announce_pics.pics_2 = pics_2
        announce_pics.pics_3 = pics_3
        announce_pics.save()

    context['form_announce'] = AnnounceForm()
    return render(request, 'user/change_pics_validation.html', context)


def change_price(request):
    """Change price is the method for get
    the cancel infos of the property"""
    context = {}
    code = request.GET.get('announce')
    code_change = request.GET.get('change')
    if request.user.is_authenticated:
        if 'change' in request.GET:
            announce = Announces.objects.filter(code=code_change)
            price_day = request.POST.get('price_day')
            price_weeks = request.POST.get('price_weeks')
            if price_day.isdigit() and price_weeks.isdigit():
                return change_price_validation(request, announce,
                                               price_day, price_weeks)
            else:
                context['error_cancel'] = 'Veuillez entrer des chiffres ' \
                                          'et/ou des nombres.'
        elif 'announce' in request.GET:
            pass
        else:
            context['error_cancel'] = 'Un problème est survenu ' \
                                      'veuillez réessayer ultérieurement.'

    else:
        context['error_cancel'] = 'Vous devez être connecté ' \
                                  'pour accéder à cette page'
    context['code'] = code
    context['form_ad'] = New_AdForm()
    context['form_announce'] = AnnounceForm()
    return render(request, 'user/change_price.html', context)


def change_price_validation(request, announce,
                            price_day, price_weeks):
    """Change price validation confirm the new price"""
    context = {}
    for info in announce:
        contact_owner(request, info)
        announce_price = Announces.objects.get(code=info.code)
        announce_price.price_day = price_day
        announce_price.price_weeks = price_day
        announce_price.save()

    context['form_announce'] = AnnounceForm()
    return render(request, 'user/change_price_validation.html', context)
