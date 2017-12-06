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

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template
from django.template.context import Context
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

import logging

logger = logging.getLogger(__name__)


class Email:
    """
    Class for sending emails
    """

    def __init__(self, subject, to_addresses, template, context=None, from_address=None, cc=None, bcc=None):
        self.subject = subject
        self.to_addresses = to_addresses

        if type(context) == dict:
            context = Context(context)
            self.html_content = Template(template).render(context)
        else:
            self.html_content = template

        self.text_content = mark_safe(strip_tags(self.html_content))

        self.from_address = settings.EMAIL_FROM if not from_address else from_address
        self.cc = cc
        self.bcc = bcc

    def send_email(self):
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.text_content,
            from_email=self.from_address,
            to=self.to_addresses,
            bcc=self.bcc,
            cc=self.cc,
            reply_to=[self.from_address, ],
        )

        email.attach_alternative(self.html_content, 'text/html')
        email.send(fail_silently=False)
