from __future__ import unicode_literals

from django.shortcuts import render

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
