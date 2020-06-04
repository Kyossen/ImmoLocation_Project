#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Here, all forms used by the platform
These forms allow communication between a user and the system
They use the text fields of the form type for this"""

# Import Django
from django import forms
from django.forms.utils import ErrorList


class ParagraphErrorList(ErrorList):
    """The first one is a response error form
    I use this form for certain answers"""
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % \
               ''.join(['<p class="small error">%s</p>' % e for e in self])


class AnnounceForm(forms.Form):
    """Announce form is the form for find a
    advertissement announce with help of the database
    This form manage l'input of the user when this execute an find"""
    announce = forms.CharField(
        label='userSearch',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)
