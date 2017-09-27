import base64
import logging

from django.conf import settings
from six.moves.urllib.parse import quote_plus, unquote_plus, parse_qsl

from gbkfit_web.models import Verification

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
    address = protocol + '://' + site_name
    if settings.ROOT_SUBDIRECTORY_PATH != '':
        address += '/' + settings.ROOT_SUBDIRECTORY_PATH[:-1]
    return address


def get_token(information):
    """
    Stores the information in the database and generates a corresponding token
    :param information: information that needs to be stored and corresponding token to be generated
    :return: token to be encoded in the url
    """
    try:
        verification = Verification.objects.create(information=information)
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
    try:
        params = dict(parse_qsl(url_unquote(token)))
        verification = Verification.objects.get(id=params.get('id'))
        return verification.information
    except Verification.DoesNotExist:
        raise ValueError('Invalid verification code')
    except Exception as e:
        logger.exception(e)  # should notify admins via email
        raise
