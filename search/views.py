#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning"""

# Import Django
from django.core.paginator import Paginator
from django.shortcuts import render

# Import file
from .forms import AnnounceForm, ParagraphErrorList
from user.models import Announces
from user.views import auto_delete_booking


def index(request):
    """Index function is a function that manage the platform base
    She get a input user and execute a find with
    the database, and result function"""
    context = {}
    # Get input user
    if request.method == 'POST':
        form = AnnounceForm(request.POST, error_class=ParagraphErrorList)
    else:
        # GET method. Create a new form to be used in the template.
        form = AnnounceForm()
    context['form_announce'] = form
    return render(request, 'search/index.html', context)


def result(request):
    """Result is the function that displays the results after a search
    With result.html she allow of display the rentals"""
    context = {}
    list_rental = []
    if request.method == 'POST':

        # Check if some reservation is to be deleted today
        auto_delete_booking(request)


        # Check if input is good
        if request.POST.get('announce') == "":
            context['form_announce'] = AnnounceForm()
            context['error_result'] = "Nous avons eu un problème, pouvez " \
                                      "vous recommencer ? Merci."
            return render(request, 'search/result.html', context, status=401)
        else:
            announce = request.POST['announce']
            # Getting a more info on food
            return result_search_city(request, announce, list_rental)

    else:
        # Check if user use a correct url when the page is the next or previous
        if 'page' in request.GET:
            announce = request.GET['search']
            return result_search_city(request, announce, list_rental)


def result_search_city(request, announce, list_rental):
    """This function is used for get information
    on the rental in the database with a filter
    (city)"""
    context = {}
    announce_city = Announces.objects.filter(city__icontains=announce)
    for annouce_result in announce_city:
        return result_search_rental(request, list_rental,
                                    annouce_result.city, context)

    if not announce_city:
        print('True')
        return result_search_country(request, announce, list_rental)


def result_search_country(request, announce, list_rental):
    """This function is used for get information
    on the rental in the database with a filter
    (country)"""
    print(request)
    context = {}
    announce = Announces.objects.filter(country__icontains=announce)
    print(announce)
    for annouce_result in announce:
        return result_search_rental(request, list_rental,
                                    annouce_result.city, context)

    if not announce:
        return error_result(request, 'not_exist')


def result_search_rental(request, list_rental, announce, context):
    """This function is used to obtain information
    on the location of the location chosen by the user"""
    context = context
    result_rental_city = Announces.objects.filter(city=announce)
    result_rental_country = Announces.objects.filter(country=announce)

    if result_rental_city:
        for search_rental in result_rental_city:
            if search_rental not in list_rental:
                list_rental.append(search_rental)
    if not result_rental_city:
        for search_rental in result_rental_country:
            if search_rental not in list_rental:
                list_rental.append(search_rental)

    context['announce_result'] = list_rental
    # Create a pagination for users.
    paginator = Paginator(list_rental, 6)
    page = request.GET.get('page', 1)
    nb_page = paginator.get_page(page)
    context['nb_page'] = nb_page
    context['announce_result'] = paginator.page(page)
    context['form_announce'] = AnnounceForm()
    # Get user info for display of the results
    if 'page' in request.GET:
        context['search'] = announce
    else:
        context['search'] = request.POST.get('announce')
    return render(request, 'search/result.html', context)


def error_result(request, error):
    """This method is a method for return
    the potential errors when run a request"""
    context = {}
    if 'not_exist' in error:
        context['form_announce'] = AnnounceForm()
        context['error_result'] = "Nous avons eu un problème, " \
                                  "pouvez vous recommencer ? Merci."
        return render(request, 'search/result.html', context, status=401)


def description(request):
    """Description is the method and the page for displaying
    more information on rental"""
    context = {}
    # Check if announce is present in the url
    announce_id = request.GET.get('announce')
    # Filter the id of the rental for be sure that is a good rental
    announce = Announces.objects.filter(code=announce_id)
    for des_announce in announce:
        if des_announce.city:
            context['announce_city'] = des_announce.city
            return description_announce(request, announce, context)
        else:
            context['error_description'] = "Nous n'avons pas d'informations " \
                                           "supplémentaires à disposition. " \
                                           "Toutes nos excuses."
            return render(request, 'search/description.html', context)
    if not announce:
        return error_load_page(request, context)


def description_announce(request, r_description, context):
    """Browse the database data and get the information
            for display in page description.html"""
    for des_rental in r_description:
        context['announce_city'] = des_rental.city
        context['announce_country'] = des_rental.country
        context['announce_img_1'] = des_rental.pics_1
        context['announce_img_2'] = des_rental.pics_2
        context['announce_img_3'] = des_rental.pics_3
        context['announce_price_day'] = des_rental.price_day
        context['announce_price_weeks'] = des_rental.price_weeks
        context['announce_description'] = des_rental.description
        context['announce_email'] = des_rental.email
        context['announce_code'] = des_rental.code
        context['form_announce'] = AnnounceForm()
        return render(request, 'search/description.html', context)


def error_load_page(request, context):
    """Check if url of the description is valid or not
    If he is not valid, this method return a error"""
    announce_city = request.GET.get('announce')
    if announce_city is None or announce_city == "":
        context['error_description'] = \
            "Nous avons eu un problème, pouvez vous recommencer ? Merci."
        context['form_announce'] = AnnounceForm()
        return render(request, 'search/description.html', context, status=200)
    else:
        context['form_announce'] = AnnounceForm()
        context['error_description'] = "Nous avons eu un problème, " \
                                       "pouvez vous recommencer ? Merci."
        return render(request, 'search/description.html', context)


def copyright_page(request):
    """Copyright page is the method for
    redirect a user to the copyright page"""
    context = {}
    context['form_announce'] = AnnounceForm()
    return render(request, 'search/copyright.html', context)
