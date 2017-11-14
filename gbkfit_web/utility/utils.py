import base64
import logging

from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from six.moves.urllib.parse import quote_plus, unquote_plus, parse_qsl

from gbkfit_web.models import Verification
from os import path, makedirs

logger = logging.getLogger(__name__)


def url_quote(raw):
    utf8 = quote_plus(raw).encode('utf8')
    return base64.b16encode(utf8).decode('utf8')


def url_unquote(enc):
    unquoted = unquote_plus(base64.b16decode(enc).decode('utf8'))
    return unquoted


def get_absolute_site_url(request):
    site_name = request.get_host()
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = settings.HTTP_PROTOCOL
    return protocol + '://' + site_name


def get_token(information, validity=None):
    """
    Stores the information in the database and generates a corresponding token
    :param information: information that needs to be stored and corresponding token to be generated
    :param validity: for how long the token will be valid (in seconds)
    :return: token to be encoded in the url
    """
    if validity:
        now = timezone.localtime(timezone.now())
        expiry = now + timedelta(seconds=validity)
    else:
        expiry = None
    try:
        verification = Verification.objects.create(information=information, expiry=expiry)
        return url_quote('id=' + verification.id.__str__())
    except:
        logger.info("Failure generating Verification token with {}".format(information))
        raise


def get_information(token):
    """
    Retrieves the information from the database for a particular token
    :param token: encoded token from email
    :return: the actual information
    """
    now = timezone.localtime(timezone.now())
    try:
        params = dict(parse_qsl(url_unquote(token)))
        verification = Verification.objects.get(id=params.get('id'), expiry__gte=now)
        if verification.verified:
            raise ValueError('Already verified')
        else:
            verification.verified = True
            verification.save()
        return verification.information
    except Verification.DoesNotExist:
        raise ValueError('Invalid or expired verification code')
    except Exception as e:
        logger.exception(e)  # should notify admins via email
        raise

def check_path(my_path):
    """
    Check if path ends with a slash ('/'). Else, it adds it.
    :param path: path
    :return: functional path
    """
    if len(my_path) > 0 and my_path[-1] != '/':
        my_path = my_path + '/'

    if not path.exists(path):
        makedirs(path)

    return path