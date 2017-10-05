from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated():
        return render(
            request,
            "base/base.html",
        )
    else:
        return render(
            request,
            "base/welcome.html",
        )
