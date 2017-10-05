from django import forms
from gbkfit_web.models import User

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init(self, *args, **kwargs):
        del self.fields['password']

    class Meta:
        model = User
        fields = ('username', 'title', 'first_name', 'last_name', 'email', 'gender', 'institution', 'is_student',
                  'country', 'scientific_interests')