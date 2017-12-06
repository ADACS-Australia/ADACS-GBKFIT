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
from gbkfit_web.models import User
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

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

class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = FIELDS
        labels = LABELS
        widgets = WIDGETS

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        try:
            self.fields['old_password'].widget.attrs.update({'class': "form-control"})
        except:
            pass
        self.fields['new_password1'].widget.attrs.update({'class': "form-control"})
        self.fields['new_password2'].widget.attrs.update({'class': "form-control"})

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password