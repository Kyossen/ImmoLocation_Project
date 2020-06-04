#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for payment app"""

# Import Django
from django.urls import reverse
from django.test import TestCase, RequestFactory

# Import files
from user.models import User, Announces
from payment.views import payment_process, payment_canceled


class PaymentPageTestCase(TestCase):
    """This class tests the payment process with Paypal"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             email_paypal='Toto@hotmail.fr',
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
            date='2020-04-30',
            email='test@hotmail.fr',
            pics_1='test',
            pics_2='test',
            pics_3='test',
            booking='',
            code=1000,
            user_id=1
        )

        self.new_announce.save()

    def test_paymentProcess_page_returns_200(self):
        """Test if user can access a payment page when
        he is connected and start a proccess payment"""
        print("Test payment page with a user connected")
        request = self.factory.get(reverse('payment_process'))
        request.user = self.user
        user = User.objects.get(pk=1)
        announce = Announces.objects.filter(code=1000)
        for info in announce:
            response = payment_process(request, info,
                                       user.email_paypal, 100)
            self.assertEqual(response.status_code, 200)

    def test_paymentCanceled_page_returns_200_1(self):
        """Test if user can access a payment page when
        he is not connected"""
        print("Test payment page with a user not connected")
        response = self.client.get(reverse('payment_canceled'))
        self.assertEqual(response.status_code, 200)

    def test_paymentCanceled_page_returns_200_2(self):
        """Test if user can access a payment page when
        he is connected"""
        print("Test payment page with a user connected")
        request = self.factory.get(reverse('payment_canceled'))
        request.user = self.user
        response = payment_canceled(request)
        self.assertEqual(response.status_code, 200)
