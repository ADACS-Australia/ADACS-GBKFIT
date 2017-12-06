"""
Source: https://www.djangosnippets.org/snippets/1019/

Adapted by DV.

Syntax: {% get_fieldset list,of,fields as new_form_object from original_form %}

note: list,of,fields doesn't allow spaces before/after comma.

Example:

{% load fieldsets %}
...
<fieldset id="contact_details">
    <legend>Contact details</legend>
    <ul>
{% get_fieldset first_name,last_name,email,cell_phone as personal_fields from form %}
{{ personal_fields.as_ul }}
    </ul>
</fieldset>

<fieldset>
    <legend>Address details</legend>
    <ul>
{% get_fieldset street_address,post_code,city as address_fields from form %}
{{ address_fields.as_ul }}
    </ul>
</fieldset>
"""

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


import copy

from django import template
from collections import OrderedDict

register = template.Library()


def get_fieldset(parser, token):
    try:
        args = token.split_contents()
        name = args[0]
        fields = args[1]
        as_ = args[2]
        variable_name = args[3]
        from_ = args[4]
        form = args[5]
        # name, fields, as_, variable_name, from_, form = args
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)


get_fieldset = register.tag(get_fieldset)


class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable

    def render(self, context):
        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)
        try:
            new_form.fields = OrderedDict(((key, value) for key, value in form.fields.items() if key in self.fields))
            context[self.variable_name] = new_form
        except:
            pass

        return u''
