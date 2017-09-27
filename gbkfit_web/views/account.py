from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gbkfit_web.forms.account.registration import RegistrationForm


def registration(request):
    data = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/registration.html",
        {
            'form': form,
            'data': data,
        }
    )


@login_required
def profile(request):
    from gbkfit_web.mailer.email import Email
    subject = 'Test Subject'
    to_addresses = ['shiblicse@gmail.com']
    context = {}
    template = 'hi'
    from_address = None
    cc = None
    bcc = None
    email = Email(subject, to_addresses, context, template, from_address=from_address)
    email.send_email()
    return render(
        request,
        "accounts/profile.html",
    )
