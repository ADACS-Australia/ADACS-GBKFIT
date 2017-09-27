from django import forms
from django.utils.translation import ugettext_lazy as _

from gbkfit_web.mailer.actions import email_verify_request
from gbkfit_web.models import User


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={'class': "form-control"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].initial = 'AU'
        self.fields['username'].help_text = None
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['scientific_interests'].help_text = 'e.g. your area of expertise, how you hope to use the data, ' \
                                                        'team memberships and collaborations'

    class Meta:
        model = User

        fields = ['title', 'first_name', 'last_name', 'email', 'gender', 'institution', 'is_student', 'country',
                  'scientific_interests', 'username', 'password']

        widgets = {
            'title': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'first_name': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'last_name': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'email': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'gender': forms.Select(
                attrs={'class': "form-control"},
            ),
            'institution': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'is_student': forms.CheckboxInput(),
            'country': forms.Select(
                attrs={'class': "form-control"},
            ),
            'scientific_interests': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'},
            ),
            'username': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'password': forms.PasswordInput(
                attrs={'class': "form-control"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(u'Passwords do not match')
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        email_verify_request(user.email, user.title, user.first_name, user.last_name, 'bingo/link/')
        if commit:
            user.save()
        return user


# class RegistrationForm(forms.Form):
#     MR = "Mr"
#     MS = "Ms"
#     MISS = "Miss"
#     MRS = "Mrs"
#     DR = "Dr"
#     PROF = "Prof"
#     A_PROF = "A/Prof"
#
#     TITLE_CHOICES = [
#         (MR, 'Mr'),
#         (MS, 'Ms'),
#         (MISS, 'Miss'),
#         (MRS, 'Mrs'),
#         (DR, 'Dr'),
#         (PROF, 'Prof'),
#         (A_PROF, 'A/Prof'),
#     ]
#     title = forms.ChoiceField(
#         label=_("Title"),
#         choices=TITLE_CHOICES,
#         widget=forms.Select(
#             attrs={'class': 'form-control'},
#         ),
#     )
#
#     first_name = forms.CharField(
#         label=_("First Name"),
#         max_length=30,
#         widget=forms.TextInput(
#             attrs={'class': "form-control"},
#         ),
#     )
#
#     last_name = forms.CharField(
#         label=_("Last Name"),
#         max_length=30,
#         widget=forms.TextInput(
#             attrs={'class': "form-control"},
#         ),
#     )
#
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=30,
#         widget=forms.EmailInput(
#             attrs={'class': "form-control"},
#         ),
#     )
#
#     MALE = "Male"
#     FEMALE = "Female"
#     PREFER_NOT_TO_SAY = "Prefer not to say"
#     GENDER_CHOICES = [
#         (MALE, 'Male'),
#         (FEMALE, 'Female'),
#         (PREFER_NOT_TO_SAY, 'Prefer not to say'),
#     ]
#     gender = forms.ChoiceField(
#         label=_("Gender"),
#         choices=GENDER_CHOICES,
#         widget=forms.Select(
#             attrs={'class': 'form-control'},
#         ),
#     )
#
#     institution = forms.CharField(
#         label=_("Institution"),
#         max_length=100,
#         widget=forms.TextInput(
#             attrs={'class': "form-control"},
#         ),
#     )
#
#     NO = 'No'
#     YES = 'Yes'
#     STUDENT_CHOICES = (
#         (NO, 'No'),
#         (YES, 'Yes'),
#     )
#     is_student = forms.ChoiceField(
#         label=_("Are you a student?"),
#         choices=STUDENT_CHOICES,
#         widget=forms.Select(
#             attrs={'class': 'form-control'},
#         ),
#     )
#
#     country = forms.ChoiceField(
#         choices=[('', 'Select Country')] + list(countries),
#         widget=forms.Select(
#             attrs={'class': 'form-control'},
#         ),
#         initial='AU',
#     )
#
#     scientific_interests = forms.CharField(
#         label=_("Scientific Interests"),
#         help_text=_("e.g. your area of expertise, how you hope to use the data, team memberships and collaborations"),
#         widget=forms.Textarea(
#             attrs={'rows': 3, 'class': 'form-control'},
#         ),
#         required=False,
#     )
#
#     username = forms.CharField(
#         label=_("Username"),
#         max_length=150,
#         widget=forms.TextInput(
#             attrs={'class': "form-control"},
#         ),
#     )
#
#     password = forms.CharField(
#         label=_("Password"),
#         widget=forms.PasswordInput(
#             attrs={'class': "form-control"}
#         ),
#     )
#
#     confirm_password = forms.CharField(
#         label=_("Confirm Password"),
#         widget=forms.PasswordInput(
#             attrs={'class': "form-control"}
#         ),
#     )
