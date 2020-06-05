#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for search app"""

# Import Django
from django.urls import reverse
from django.test import TestCase, RequestFactory

# Import file
from user.models import Announces
from user.models import User
from search.views import description_announce


class IndexPageTestCase(TestCase):
    """This class tests whether the index
    page returns a 200 status code"""

    def test_index_page(self):
        """Test the home page (index)"""
        print("Test the home page (index)")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_search(self):
        """Test the search on index"""
        print("Test the search on index")
        response = self.client.post(reverse('index'), {'announce': 'NotExist'})
        self.assertEqual(response.status_code, 200)


class CopyrightPageTestCase(TestCase):
    """This class tests whether the copyright
    page returns a 200 status code"""

    def test_copyright_page(self):
        """Test the copyright page"""
        print("Test the copyright page")
        response = self.client.get(reverse('copyright'))
        self.assertEqual(response.status_code, 200)


class ResultPageTestCase(TestCase):
    """This class tests whether the result page
    returns a 200 status code if a announce is found or not"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.user = User.objects.create_user(pk=1,
                                             first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

    def test_result_find_page_returns_200(self):
        """This method create a announce in the database
        and test if user can the find this announce"""
        print("Test for find a announce. Announce is found.")
        announce = Announces.objects.create(title='TestAnnounce',
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
                                            code=150,
                                            user_id=1)
        announce.save()
        response = self.client.post(reverse('result'),
                                    {'announce': announce.city})
        self.assertEqual(response.status_code, 200)

    def test_result_page_returns_notExist(self):
        """Test if announce not is find or not exist"""
        print("Test for find a announce. Announce is not found.")
        try:
            response = self.client.post(reverse('result'),
                                        {'announce': 'NotExist'})
            self.assertEqual(response.status_code, 401)
        except ValueError:
            raise ValueError("Check line 77. "
                             "Missing a letter or something else "
                             "in the parameter")


class DescriptionPageTestCase(TestCase):
    """This class tests whether the description page
    returns a status code 200 if an announce is found or not
    via its code"""

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

    def test_description_find_page_returns_200(self):
        """Test with a good code"""
        print("Test for description page with a good code")
        announce = Announces.objects.create(title='TestAnnounce',
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
                                            code=150,
                                            user_id=1)
        announce.save()
        response = self.client.post(reverse('description'),
                                    {'announce': announce.code})
        self.assertEqual(response.status_code, 200)

    def test_getDescriptionInfo_page_return_200(self):
        """This test is to get the infos on the description rental"""
        print('Get info description rental')
        announce = Announces.objects.create(title='TestAnnounce',
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
                                            code=150,
                                            user_id=1)
        announce.save()

        request = self.factory.get(reverse('description'),
                                   {'announce': 150})
        request.user = self.user
        context = {}
        announce_id = request.GET.get('announce')
        announce = Announces.objects.filter(code=announce_id)

        response = description_announce(request, announce, context)
        self.assertEqual(response.status_code, 200)
