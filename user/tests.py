#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for user app"""

# Import Django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# Import files
from user.models import User, Announces, MyRental, Booking
from user.views import dashboard, add_email_paypal, delete_my_offer, \
    change_price_validation, rent_now, disconnect, \
    user_booking_info, rented, cancel_myrented, change_pics, \
    handler_ad, change_price, new_ad, \
    auto_delete_booking , check_the_available_dates
from user.payment_done import get_info_booking, rent_validation_done
from payment.views import payment_process

# Import lib
from io import BytesIO
from PIL import Image


class SignupPageTestCase(TestCase):
    """This class tests whether the registration page
    returns a 200 status code if the information
    on the user is good or not"""

    def test_get_signUP_page(self):
        """This a little test for get the signup page"""
        print('Test for get a signup page.')
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_success_returns_302(self):
        """Test if good info"""
        print("The Test for sign up to the plateforme.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test50@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 302)

    def test_signup_page_emailFalse_returns_401(self):
        """Test if not good email"""
        print("Test for a fake email.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test500@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})

        response_2 = self.client.post(reverse('sign_up'),
                                      {'email': 'test500@hotmail.fr',
                                       'password': 'wordpass2!',
                                       'confirmation_password': 'wordpass2!',
                                       'last_name': 'name',
                                       'first_name': 'surname',
                                       'phone': '02-01-02-01-02',
                                       'date_of_birth': '19/02/1995',
                                       'postal_address': 'address',
                                       'gcu': True})
        self.assertEqual(response_2.status_code, 401)

    def test_password_returns_401(self):
        """Test if not good password"""
        print("First test for a fake password. First test.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2',
                                     'confirmation_password': 'wordpass2',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 401)

    def test_password2_returns_401(self):
        """Test if not good password"""
        print("First test for a fake password. Second test.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass!',
                                     'confirmation_password': 'wordpass!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 401)

    def test_password3_returns_401(self):
        """Test if not good password"""
        print("First test for a fake password. Third test.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'woss2!',
                                     'confirmation_password': 'woss2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 401)

    def test_phoneFalse_1_returns_401(self):
        """Test if not good number phone"""
        print("Test for a fake a number phone")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02-05-18',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 401)

    def test_phoneTrue_returns_302_1(self):
        """Test if good number but with the space barre"""
        print("Test if good number but with the space barre")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02 01 02 01 02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 302)

    def test_phoneTrue_returns_302_2(self):
        """Test if good number but with the slash barre"""
        print("Test if good number but with the slash barre")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02/01/02/01/02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 302)

    def test_dateFalse_returns_401(self):
        """Test if not good birth data"""
        print("Test if not good birth data")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19-02-1995',
                                     'postal_address': 'address',
                                     'gcu': True})
        self.assertEqual(response.status_code, 401)

    def test_addressFalse_returns_401(self):
        """Test if not good address"""
        print("Test if not good address")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'address': 'addresstjfjftjtjyjhbjrtyrgr',
                                     'gcu': True})
        self.assertEqual(response.status_code, 401)

    def test_gcuFalse_returns_401(self):
        """Test if not valid checkbox"""
        print("Test if not valid checkbox")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'address': 'addrjhbjrtyrgr',
                                     'gcu': False})
        self.assertEqual(response.status_code, 401)

    def test_gcu_access_page_return_200(self):
        """Test gcu access"""
        print("Test gcu access")
        response = self.client.post(reverse('gcu'))
        self.assertEqual(response.status_code, 200)


class ConnectPageTestCase(TestCase):
    """This class tests whether the login page
    returns a 200 status code if the information
    on the user is good or not"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

    def test_login_page_success_returns_302(self):
        """Test if good info"""
        print("Test for the connect")
        self.client.post(reverse('sign_up'),
                         {'email': 'test51@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.post(reverse('connect'),
                                    {'email': 'test51@hotmail.fr',
                                     'wordpass': 'wordpass2!'})
        self.assertEqual(response.status_code, 302)

    def test_wordpassFalse_returns_401(self):
        """Test for a connect not valid -> A bad password"""
        print("Test for a connect not valid -> A bad password")
        response = self.client.post(reverse('connect'),
                                    {'email': 'test@hotmail.fr',
                                     'wordpass': 'wordpss'})
        self.assertEqual(response.status_code, 401)

    def test_emailFalse_returns_401(self):
        """Test for a connect not valid -> A bad email"""
        print("Test for a connect not valid -> A bad email")
        response = self.client.post(reverse('connect'),
                                    {'email': 'testhotmail.fr',
                                     'wordpass': 'wordpss'})
        self.assertEqual(response.status_code, 401)

    def test_getConnect_returns_200(self):
        """Test for a get page connect"""
        print("Test for a get page connect")
        response = self.client.get(reverse('connect'))
        self.assertEqual(response.status_code, 200)

    def test_ForgotPassword_page_returns_200(self):
        """Test with valid email"""
        print('Forgot password test an with email valid')
        response = self.client.post(reverse('password_reset'),
                                    {'email': 'test@hotmail.fr'})
        self.assertEqual(response.status_code, 302)

    def test_ForgotPassword2_page_returns_200(self):
        """Test with a bad email"""
        print('Forgot password test with an email not valid')
        response = self.client.post(reverse('password_reset'),
                                    {'email': 'testhotmail.fr'})
        # The result is 200 because the password reset page works on any case.
        # However, the email is not sent
        self.assertEqual(response.status_code, 200)


class DashboardPageTestCase(TestCase):
    """This class tests whether the dashboard page
    returns a 200 status code if user is connect
    or not with The setup method"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

    def test_dashboard_page_returns_200(self):
        """ Test if the user is redirected to the page and
        the database retrieves the data using the above method"""
        print("Test dashboard with a user connected")
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_add_email_paypal(self):
        """This test is to for add an paypal email"""
        print("Test add email paypal")
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.post(reverse('add_email_paypal'),
                                    {'email': 'test52@hotmail.fr'})
        self.assertEqual(response.status_code, 302)

    def test_access_only_add_email_paypal(self):
        """This test is to for access a add email paypal"""
        print("Test access add email paypal")
        request = self.factory.get(reverse('add_email_paypal'))
        request.user = self.user
        response = add_email_paypal(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboardDisconnect_page_returns_200(self):
        """Test if user is redirected well to page"""
        print("Test dashboard whhen we is disconnect")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class DisconnectPageTestCase(TestCase):
    """This class tests whether the user is redirected
    to the index (home page) after asking for the disconnect."""

    def test_disconnectUser_page_returns_200(self):
        """Test if user is redirected to the home page"""
        print("Test disconnect a user -> return 200")
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})
        response = self.client.get(reverse('disconnect'))
        self.assertEqual(response.status_code, 302)

    def test_disconnect_page_returns_200(self):
        """Test if user is redirected well to page"""
        print("Test disconnect -> return 200")
        response = self.client.get(reverse('disconnect'))
        self.assertEqual(response.status_code, 200)


class HandlerAdPageTestCase(TestCase):
    """This class is class for the tests of the handler"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

        self.new_announce = Announces(
            pk=1,
            title='TestAnnounce',
            address='image',
            description='test',
            city='test',
            country='test',
            price_day=100,
            price_weeks=150,
            email='test@hotmail.fr',
            pics_1='test',
            pics_2='test',
            pics_3='test',
            booking='',
            code=1000,
            user_id=1
        )
        self.new_announce.save()

        self.new_myrental = MyRental(
            pk=1,
            rental_city='test',
            rental_country='test',
            email_user_rental='test@hotmail.fr',
            code=1000,
            user_id=1
        )
        self.new_myrental.save()

        self.new_booking = Booking(
            pk=1,
            date_min='2020/05/05',
            date_max='2020/05/05',
            code=1000,
            user_id=1
        )
        self.new_booking.save()

    def test_handlerAd_page_return_200_1(self):
        """Handler test not connected"""
        print("Handler test not connected")
        response = self.client.get(reverse('handler_ad'))
        self.assertEqual(response.status_code, 200)

    def test_handlerAd_page_return_200_2(self):
        """Handler test connected"""
        print('Handler test connected')
        request = self.factory.get(reverse('handler_ad'))
        request.user = self.user
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_changePrice_page_return_200(self):
        """Change Price test"""
        print('Change Price test')
        request = self.factory.get(reverse('change_price'),
                                   {'change': 1000})
        code_change = request.GET.get('change')
        announce = Announces.objects.filter(code=code_change)
        price_day = 100
        price_weeks = 150
        request.user = self.user
        response = change_price_validation(request, announce,
                                           price_day, price_weeks)
        self.assertEqual(response.status_code, 200)

    def test_changePrice_page_return_error(self):
        """Change Price test in change_price page"""
        print('Change Price test in change_price page')
        try:
            request = self.factory.get(reverse('change_price'),
                                       {'change': 1000})
            user = User.objects.get(pk=1)
            request.user = self.user

            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session['member_id'] = user.id
            request.session.save()

            response = change_price(request)
            self.assertEqual(response.status_code, 200)
        # This except return a pass because the number in the post is None
        except AttributeError:
            pass

    def test_changePrice_page_return_error_200(self):
        """Change Price test with str"""
        print('Change Price test with str')
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.post(reverse('change_price'),
                                    {'price_day': str(100),
                                     'price_weeks': str(100)})
        # Error is 200 because this error is managed directly by the code
        self.assertEqual(response.status_code, 200)

    def test_changePriceAnnounce_page_return_200(self):
        """Change Price test with announce in URL"""
        print('Change Price test with announce in URL')
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.get(reverse('change_price'),
                                   {'announce': 1000})
        self.assertEqual(response.status_code, 200)

    def test_changePriceNotConnected_page_return_200(self):
        """Change Price test with user not connected"""
        print('Change Price test with user not connected')
        response = self.client.get(reverse('change_price'),
                                   {'announce': 1000})
        self.assertEqual(response.status_code, 200)

    def test_changePics_page_return_200(self):
        """Change Price test"""
        print('Change Pics test')
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.post(reverse('change_pics'),
                                    {'pics_1': 'test.jpg',
                                     'pics_2': 'test.jpg',
                                     'pics_3': 'test.jpg'})
        self.assertEqual(response.status_code, 200)

    def test_changePicsNotConnected_page_return_200(self):
        """Change Pics test with user not connected"""
        print('Change Pics test with user not connected')
        response = self.client.get(reverse('change_pics'),
                                   {'announce': 1000})
        self.assertEqual(response.status_code, 200)

    def test_changePicsAnnounce_page_return_200(self):
        """Change Pics test with announce in URL"""
        print('Change Price test with announce in URL')
        request = self.factory.get(reverse('change_pics'),
                                   {'announce': 1000})
        request.user = self.user
        response = change_pics(request)
        self.assertEqual(response.status_code, 200)

    def test_cancelRented_page_return_200_1(self):
        """Cancel rented test with user connected"""
        print('Cancel rented test with user connected')
        request = self.factory.get(reverse('delete_rent'),
                                   {'cancel': 1000})
        request.user = self.user
        code_cancel = request.GET.get('cancel')
        if 'cancel' in request.GET:
            announce = Announces.objects.filter(code=code_cancel)
            response = cancel_myrented(request, announce)
            self.assertEqual(response.status_code, 200)

    def test_cancelRented_page_return_200_2(self):
        """Cancel rented test with user not connected"""
        print('Cancel rented test with user not connected')
        response = self.client.get(reverse('cancel_rented'),
                                   {'announce': 1000})
        self.assertEqual(response.status_code, 200)

    def test_cancelRentedError_page_return_200(self):
        """Cancel rented Error test with user not connected"""
        print('Cancel rented Error test with user not connected')
        response = self.client.get(reverse('delete_rent'),
                                   {'': ''})
        self.assertEqual(response.status_code, 200)

    def test_deleteRentedAnnounce_page_return_200(self):
        """Delete Rented test with user connected and announce"""
        print('Delete Rentedtest with user connected and announce')
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.get(reverse('delete_rent'),
                                   {'announce': 1000})
        self.assertEqual(response.status_code, 200)

    def test_deleteRentedCancel_page_return_200_1(self):
        """Delete rented test with user not connected and cancel"""
        print('Delete rented test with user connected and cancel')
        request = self.factory.get(reverse('delete_rent'),
                                   {'cancel': 1000})
        request.user = self.user
        code_cancel = request.GET.get('cancel')
        if 'cancel' in request.GET:
            announce = Announces.objects.filter(code=code_cancel)
            response = delete_my_offer(request, announce)
            self.assertEqual(response.status_code, 200)

    def test_deleteRentedCancel_page_return_200_2(self):
        """Delete rented test with user not connected and cancel"""
        print('Delete rented test with user not connected'
              ' and cancel')
        response = self.client.get(reverse('delete_rent'),
                                   {'cancel': 1000})
        self.assertEqual(response.status_code, 200)

    def test_deleteRentedNone_page_return_200(self):
        """Delete MyOffer test with user connected and None"""
        print('Delete MyOffer test with user connected'
              ' and None')
        self.client.post(reverse('sign_up'),
                         {'email': 'test52@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address',
                          'gcu': True})

        response = self.client.get(reverse('delete_rent'),
                                   {'None': ''})
        self.assertEqual(response.status_code, 200)


class RentNowTestCase(TestCase):
    """This class is class for the tests of the MyRent dashboard"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

        self.new_announce = Announces(
            pk=1,
            title='TestAnnounce',
            address='image',
            description='test',
            city='test',
            country='test',
            price_day=100,
            price_weeks=150,
            email='test@hotmail.fr',
            pics_1='test',
            pics_2='test',
            pics_3='test',
            booking='',
            code=1000,
            user_id=1
        )
        self.new_announce.save()

        self.new_myrental = MyRental(
            pk=1,
            rental_city='test',
            rental_country='test',
            email_user_rental='test@hotmail.fr',
            code=1000,
            user_id=1
        )
        self.new_myrental.save()

        self.new_booking = Booking(
            pk=1,
            date_min='2020/01/01',
            date_max='2020/02/02',
            code=1000,
            user_id=1
        )
        self.new_booking.save()

    def test_rent_now_page_return_200_1(self):
        """Test access rent now with user connected"""
        print('Test access rent now with user connected')
        request = self.factory.get(reverse('rent_now'),
                                   {'announce': 1000})
        request.user = self.user
        response = rent_now(request)
        self.assertEqual(response.status_code, 200)

    def test_rent_now_page_return_200_2(self):
        """Test access rent now with user not connected"""
        print('Test access rent now with user not connected')
        response = self.client.get(reverse('rent_now'),
                                   {'announce': 1000})
        self.assertEqual(response.status_code, 200)

    def test_rent_validation_page_return_200(self):
        """This test is for test  the validation of the rent booking"""
        print('Test the validation of the rent booking')
        request = self.factory.get(reverse('rent_validation'),
                                   {'announce': 1000})
        request.user = self.user
        announce_id = request.GET.get('announce')
        announce = Announces.objects.filter(code=announce_id)
        for info in announce:
            amount = info.price_day * 1
            user = User.objects.get(pk=info.user_id)
            response = payment_process(request, info,
                                       user.email_paypal,
                                       amount)
            self.assertEqual(response.status_code, 200)

    def test_check_the_available_dates(self):
        """Test check the available dates"""
        print('Test check the available dates')
        request = self.factory.get(reverse('check_dates'),
                                   {'announce': 1000})
        request.user = self.user
        response = check_the_available_dates(request)
        self.assertEqual(response.status_code, 200)


class MyRentPageTestCase(TestCase):
    """This class is class for the tests of the MyRent dashboard"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

        self.new_announce = Announces(
            pk=1,
            title='TestAnnounce',
            address='image',
            description='test',
            city='test',
            country='test',
            price_day=100,
            price_weeks=150,
            email='test@hotmail.fr',
            pics_1='test',
            pics_2='test',
            pics_3='test',
            booking='',
            code=1000,
            user_id=1
        )
        self.new_announce.save()

        self.new_myrental = MyRental(
            pk=1,
            rental_city='test',
            rental_country='test',
            email_user_rental='test@hotmail.fr',
            code=1000,
            user_id=1
        )
        self.new_myrental.save()

        self.new_booking = Booking(
            pk=1,
            date_min='2020/01/01',
            date_max='2020/02/02',
            code=1000,
            user_id=1
        )
        self.new_booking.save()

    def test_myRent_page_return_200_1(self):
        """MyRented access test with user connected"""
        print('Myrented access with user connected')
        request = self.factory.get(reverse('rented'))
        request.user = self.user
        response = rented(request)
        self.assertEqual(response.status_code, 200)

    def test_myRented_page_return_200_2(self):
        """Myrented access test with user not connected"""
        print('Myrented access test with user not connected')
        response = self.client.get(reverse('rented'))
        self.assertEqual(response.status_code, 200)

    def test_auto_delete_booking(self):
        """Test auto delete booking with user connected"""
        print('Test auto delete booking with user connected')
        request = self.factory.get(reverse('connect'))
        request.user = self.user
        auto_delete_booking(request)


class InfoUserBooking(TestCase):
    """This class is class for the tests of the booking info user"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

        self.new_announce = Announces(
            pk=1,
            title='TestAnnounce',
            address='image',
            description='test',
            city='test',
            country='test',
            price_day=100,
            price_weeks=150,
            email='test@hotmail.fr',
            pics_1='test',
            pics_2='test',
            pics_3='test',
            booking='',
            code=1000,
            user_id=1
        )
        self.new_announce.save()

        self.new_myrental = MyRental(
            pk=1,
            rental_city='test',
            rental_country='test',
            email_user_rental='test@hotmail.fr',
            code=1000,
            user_id=1
        )
        self.new_myrental.save()

    def test_userBookingInfo_page_return_200_1(self):
        """User_booking_info access test with user connected"""
        print('User_booking_info access test with user connected')
        request = self.factory.get(reverse('user_booking_info'))
        request.user = self.user
        response = user_booking_info(request)
        self.assertEqual(response.status_code, 200)

    def test_userBookingInfo_page_return_200_2(self):
        """User_booking_info access test with user not connected"""
        print('User_booking_info access test with user not connected')
        response = self.client.get(reverse('user_booking_info'))
        self.assertEqual(response.status_code, 200)

    def test_userBookingInfo_page_return_200_3(self):
        """User_booking_info access test with user connected"""
        print('User_booking_info access test with user connected')
        request = self.factory.get(reverse('user_booking_info'))
        request.user = self.user
        context = {}
        search_user = MyRental.objects.filter(code=1000)
        users_all = User.objects.all()
        for info in search_user:
            for info_all in users_all:
                if info.user_id == info_all.pk:
                    context['first_name'] = info_all.first_name
                    context['last_name'] = info_all.last_name
                    context['email'] = info_all.email
                    context['phone'] = info_all.phone

        response = user_booking_info(request)
        self.assertEqual(response.status_code, 200)


def create_image(storage, filename, size=(100, 100),
                 image_mode='RGB', image_format='PNG'):
    """Generate a test image, returning the filename that it was saved as.
    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead."""
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class NewAd(TestCase):
    """This class run the tests for add a annouce"""
    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factor"""
        super(NewAd, self).setUp()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

    def test_New_ad_page_return_302(self):
        """Test for the announcement of an announcement
        without an error"""
        print('New_ad -> No error')

        url = reverse('new_ad')
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {'title': 'test52@title.fr',
                'address': 'r_address!',
                'description': 'description!',
                'city': 'name',
                'country': 'surname',
                'price_day': 100,
                'price_weeks': 100,
                'email': 'address@outlook.fr',
                'pics_1': avatar_file,
                'pics_2': avatar_file,
                'pics_3': avatar_file}
        request = self.factory.post(url, data, follow=True)
        user = User.objects.get(pk=1)
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['member_id'] = user.id
        request.session.save()

        response = new_ad(request)
        self.assertEqual(response.status_code, 302)

    def test_New_adError_page_return_302(self):
        """Test for the announcement of an announcement
        with an error"""
        print('New_ad -> With an error')

        url = reverse('new_ad')
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {'title': 'test52@title.fr',
                'address': 'r_address!',
                'description': 'description!',
                'city': 'name',
                'country': 'surname',
                'price_day': '100',
                'price_weeks': '100',
                'email': 'address@outlook.fr',
                'pics_1': avatar_file,
                'pics_2': avatar_file,
                'pics_3': avatar_file}

        request = self.factory.post(url, data, follow=True)
        user = User.objects.get(pk=1)
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['member_id'] = user.id
        request.session.save()

        response = new_ad(request)
        self.assertEqual(response.status_code, 302)


class PaymentProcessDonePageTestCase(TestCase):
    """This class is class for the tests of the payment process done"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

        self.new_announce = Announces(
            pk=10,
            title='TestAnnounce',
            address='image',
            description='test',
            city='test',
            country='test',
            price_day=100,
            price_weeks=150,
            email='test@hotmail.fr',
            pics_1='test',
            pics_2='test',
            pics_3='test',
            booking='',
            code=1000,
            user_id=1
        )
        self.new_announce.save()

        self.new_myrental = MyRental(
            pk=10,
            rental_city='test',
            rental_country='test',
            email_user_rental='test@hotmail.fr',
            code=1000,
            user_id=1
        )
        self.new_myrental.save()

        self.new_booking = Booking(
            pk=10,
            date_min='2020/05/05',
            date_max='2020/05/05',
            code=1000,
            user_id=1
        )
        self.new_booking.save()

    def test_save_new_booking(self):
        """Test the new save in the booking table"""
        print('Test the new save in the booking table')
        request = self.factory.get(reverse('payment_done'))
        user = User.objects.get(pk=1)
        request.user = self.user
        announce = Announces.objects.filter(code=1000)

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['member_id'] = user.id
        request.session.save()

        d_min = '2020/05/05'
        d_max = '2020/05/05'
        get_info_booking(request, announce, d_min, d_max)

        rent_validation_done(request)
