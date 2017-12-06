#==============================================================================
#
# This code was developed as part of the Astronomy Data and Computing Services
# (ADACS; https:#adacs.org.au) 2017B Software Support program.
#
# Written by: Dany Vohl, Lewis Lakerink, Shibli Saleheen
# Date:       December 2017
#
# It is distributed under the MIT (Expat) License (see https:#opensource.org/):
#
# Copyright (c) 2017 Astronomy Data and Computing Services (ADACS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#==============================================================================

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from gbkfit_web.models import User


FIELDS = ['title', 'first_name', 'last_name', 'email', 'gender', 'institution', 'is_student', 'country',
          'scientific_interests', 'username', ]

WIDGETS = {
            'title': forms.Select(
                attrs={'class': 'form-control', 'tabindex': '1'},
            ),
            'first_name': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '2'},
            ),
            'last_name': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '3'},
            ),
            'email': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '4'},
            ),
            'gender': forms.Select(
                attrs={'class': "form-control", 'tabindex': '5'},
            ),
            'institution': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '6'},
            ),
            'is_student': forms.CheckboxInput(
                attrs={'tabindex': '7'},
            ),
            'country': forms.Select(
                attrs={'class': "form-control", 'tabindex': '8'},
            ),
            'scientific_interests': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'tabindex': '9'},
            ),
            'username': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '10'},
            ),
        }

LABELS = {
    'title': _('Title'),
    'first_name': _('First name'),
    'last_name': _('Last name'),
    'email': _('Email'),
    'gender': _('Gender'),
    'institution': _('Institution'),
    'is_student': _('Is student?'),
    'country': _('Country'),
    'scientific_interests': _('Scientific interests'),
    'username': _('Username'),
}

class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].initial = 'AU'
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'tabindex': '11'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'tabindex': '12'})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['scientific_interests'].help_text = 'e.g. your area of expertise, how you hope to use the data, ' \
                                                        'team memberships and collaborations'

    class Meta:
        model = get_user_model()
        fields = FIELDS
        labels = LABELS
        widgets = WIDGETS

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This email address is already taken by some other user.')
        return email

    def save(self, commit=True):
        # Save the user as an inactive user
        user = super(RegistrationForm, self).save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
