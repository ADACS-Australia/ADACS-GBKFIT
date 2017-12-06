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

from django.shortcuts import render
from six.moves.urllib import parse

from gbkfit_web.models import User
from gbkfit_web.utility import utils


def verify(request):
    data = {}
    code_encrypted = request.GET.get('verification_code', None)
    if code_encrypted:
        try:
            code = utils.get_information(code_encrypted)
            params = dict(parse.parse_qsl(code))
            verify_type = params.get('type', None)
            if verify_type == 'user':
                username = params.get('username', None)
                try:
                    user = User.objects.get(username=username)
                    user.status = user.VERIFIED
                    user.is_active = True
                    user.save()
                    data.update(
                        success=True,
                        message='The email address has been verified successfully',
                    )
                except User.DoesNotExist:
                    data.update(
                        success=False,
                        message='The requested user account to verify does not exist',
                    )
        except ValueError as e:
            # This may be a variant between versions...
            try:
                data.update(
                    success=False,
                    message=e.message if e.message else 'Invalid verification code',
                )
            except:
                data.update(
                    success=False,
                    message=e if e else 'Invalid verification code',
                )
    else:
        data.update(
            success=False,
            message='Invalid Verification Code',
        )
    return render(
        request,
        "accounts/notification.html",
        {
            'type': 'email_verify',
            'data': data,
        },
    )
