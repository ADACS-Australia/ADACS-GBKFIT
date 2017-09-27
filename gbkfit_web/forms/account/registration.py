from django import forms
from django.utils.translation import ugettext_lazy as _

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
        # Set the user as an in active user until the email address is verified
        user.is_active = False
        if commit:
            user.save()
        return user
