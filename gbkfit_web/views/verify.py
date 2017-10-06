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
            data.update(
                success=False,
                message=e.message if e.message else 'Invalid verification code',
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