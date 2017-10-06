from django import forms
from gbkfit_web.models import User

class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # self.fields['username'] = forms.CharField(required=True)
        # self.fields['username'].help_text = None
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'title', 'first_name', 'last_name', 'email', 'gender', 'institution', 'is_student',
                  'country', 'scientific_interests')

        widgets = {
            'username': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '1'},
            ),
            'title': forms.Select(
                attrs={'class': 'form-control', 'tabindex': '2'},
            ),
            'first_name': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '3'},
            ),
            'last_name': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '4'},
            ),
            'email': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '5'},
            ),
            'gender': forms.Select(
                attrs={'class': "form-control", 'tabindex': '6'},
            ),
            'institution': forms.TextInput(
                attrs={'class': "form-control", 'tabindex': '7'},
            ),
            'is_student': forms.CheckboxInput(
                attrs={'tabindex': '8'},
            ),
            'country': forms.Select(
                attrs={'class': "form-control", 'tabindex': '9'},
            ),
            'scientific_interests': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'tabindex': '10'},
            ),
        }