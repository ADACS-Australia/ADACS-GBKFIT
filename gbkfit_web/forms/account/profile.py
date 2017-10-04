from django import forms
from django.contrib.auth.forms import UserChangeForm
from gbkfit_web.models import User

class EditProfileForm(UserChangeForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init(self, *args, **kwargs):
        del self.fields['password']

    class Meta:
        model = User
        fields = ('username', 'title', 'first_name', 'last_name', 'email', 'gender', 'institution', 'is_student',
                  'country', 'scientific_interests', 'password')

    # def clean_email(self):
    #     username = self.cleaned_data.get('username')
    #     email = self.cleaned_data.get('email')
    #
    #     if email and User.objects.filter(email=email).exclude(username=username).count():
    #         raise forms.ValidationError(
    #             'This email address is already in use. Please supply a different email address.')
    #     return email
    #
    # def save(self, commit=True):
    #     user = super(EditProfileForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #
    #     if commit:
    #         user.save()
    #
    #     return user