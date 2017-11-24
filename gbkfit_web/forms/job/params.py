from django import forms
from django.utils.translation import ugettext_lazy as _
from gbkfit_web.models import ParameterSet, Job, GalaxyModel, Fitter

# For convenience
XO_FIELDS = ['xo_fixed', 'xo_value', 'xo_min', 'xo_max', 'xo_wrap', 'xo_step', 'xo_relstep', 'xo_side',]
YO_FIELDS = ['yo_fixed', 'yo_value', 'yo_min', 'yo_max', 'yo_wrap', 'yo_step', 'yo_relstep', 'yo_side',]
PA_FIELDS = ['pa_fixed', 'pa_value', 'pa_min', 'pa_max', 'pa_wrap', 'pa_step', 'pa_relstep', 'pa_side',]
INCL_FIELDS = ['incl_fixed', 'incl_value', 'incl_min', 'incl_max', 'incl_wrap', 'incl_step', 'incl_relstep', 'incl_side',]
VSYS_FIELDS = ['vsys_fixed', 'vsys_value', 'vsys_min', 'vsys_max', 'vsys_wrap', 'vsys_step', 'vsys_relstep', 'vsys_side',]
VSIG_FIELDS = ['vsig_fixed', 'vsig_value', 'vsig_min', 'vsig_max', 'vsig_wrap', 'vsig_step', 'vsig_relstep', 'vsig_side',]
I0_FIELDS = ['i0_fixed', 'i0_value', 'i0_min', 'i0_max', 'i0_wrap', 'i0_step', 'i0_relstep', 'i0_side',]
R0_FIELDS = ['r0_fixed', 'r0_value', 'r0_min', 'r0_max', 'r0_wrap', 'r0_step', 'r0_relstep', 'r0_side',]
RT_FIELDS = ['rt_fixed', 'rt_value', 'rt_min', 'rt_max', 'rt_wrap', 'rt_step', 'rt_relstep', 'rt_side',]
VT_FIELDS = ['vt_fixed', 'vt_value', 'vt_min', 'vt_max', 'vt_wrap', 'vt_step', 'vt_relstep', 'vt_side',]
A_FIELDS = ['a_fixed', 'a_value', 'a_min', 'a_max', 'a_wrap', 'a_step', 'a_relstep', 'a_side',]
B_FIELDS = ['b_fixed', 'b_value', 'b_min', 'b_max', 'b_wrap', 'b_step', 'b_relstep', 'b_side',]

FIELDS_LISTS = [XO_FIELDS, YO_FIELDS, PA_FIELDS, INCL_FIELDS, VSYS_FIELDS, VSIG_FIELDS,
               I0_FIELDS, R0_FIELDS, RT_FIELDS, VT_FIELDS, A_FIELDS, B_FIELDS]

FIELDS = []
for fields_list in FIELDS_LISTS:
    for field in fields_list:
        FIELDS.append(field)

WIDGETS= {
            # xo
            'xo_fixed': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'xo_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'xo_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'xo_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'xo_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'xo_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'xo_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'xo_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # yo
            'yo_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'yo_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'yo_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'yo_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'yo_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'yo_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'yo_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'yo_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # pa
            'pa_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'pa_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'pa_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'pa_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'pa_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'pa_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'pa_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'pa_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # incl
            'incl_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'incl_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'incl_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'incl_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'incl_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'incl_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'incl_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'incl_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # vsys
            'vsys_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'vsys_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsys_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsys_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsys_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'vsys_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsys_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsys_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # vsig
            'vsig_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'vsig_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsig_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsig_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsig_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'vsig_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsig_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vsig_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            'i0_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'i0_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'i0_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'i0_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'i0_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'i0_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'i0_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'i0_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # r0
            'r0_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'r0_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'r0_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'r0_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'r0_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'r0_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'r0_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'r0_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # rt
            'rt_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'rt_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'rt_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'rt_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'rt_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'rt_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'rt_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'rt_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # vt
            'vt_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'vt_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vt_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vt_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vt_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'vt_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vt_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'vt_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
    
            # a
            'a_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'a_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'a_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'a_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'a_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'a_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'a_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'a_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),

            # b
            'b_fixed': forms.CheckboxInput(
              attrs={'class': 'has-popover'},
            ),
            'b_value': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'b_min': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'b_max': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'b_wrap': forms.CheckboxInput(
               attrs={'class': 'has-popover'},
            ),
            'b_step': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'b_relstep': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
            'b_side': forms.TextInput(
                attrs={'class': 'form-control has-popover'},
            ),
        }

LABELS = {
    #xo
    'xo_fixed': _('Fixed'),
    'xo_value': _('Value'),
    'xo_min': _('Minimum'),
    'xo_max': _('Maximum'),
    'xo_wrap': _('Wrap around'),
    'xo_step': _('Step'),
    'xo_relstep':_('Relative step'),
    'xo_side':_('Derivative sidedness'),

    #yo
    'yo_fixed': _('Fixed'),
    'yo_value': _('Value'),
    'yo_min': _('Minimum'),
    'yo_max': _('Maximum'),
    'yo_wrap': _('Wrap around'),
    'yo_step': _('Step'),
    'yo_relstep':_('Relative step'),
    'yo_side':_('Derivative sidedness'),

    #pa
    'pa_fixed': _('Fixed'),
    'pa_value': _('Value'),
    'pa_min': _('Minimum'),
    'pa_max': _('Maximum'),
    'pa_wrap': _('Wrap around'),
    'pa_step': _('Step'),
    'pa_relstep':_('Relative step'),
    'pa_side':_('Derivative sidedness'),

    #incl
    'incl_fixed': _('Fixed'),
    'incl_value': _('Value'),
    'incl_min': _('Minimum'),
    'incl_max': _('Maximum'),
    'incl_wrap': _('Wrap around'),
    'incl_step': _('Step'),
    'incl_relstep':_('Relative step'),
    'incl_side':_('Derivative sidedness'),
    
    #vsys
    'vsys_fixed': _('Fixed'),
    'vsys_value': _('Value'),
    'vsys_min': _('Minimum'),
    'vsys_max': _('Maximum'),
    'vsys_wrap': _('Wrap around'),
    'vsys_step': _('Step'),
    'vsys_relstep':_('Relative step'),
    'vsys_side':_('Derivative sidedness'),

    #vsig
    'vsig_fixed': _('Fixed'),
    'vsig_value': _('Value'),
    'vsig_min': _('Minimum'),
    'vsig_max': _('Maximum'),
    'vsig_wrap': _('Wrap around'),
    'vsig_step': _('Step'),
    'vsig_relstep':_('Relative step'),
    'vsig_side':_('Derivative sidedness'),

    'i0_fixed': _('Fixed'),
    'i0_value': _('Value'),
    'i0_min': _('Minimum'),
    'i0_max': _('Maximum'),
    'i0_wrap': _('Wrap around'),
    'i0_step': _('Step'),
    'i0_relstep':_('Relative step'),
    'i0_side':_('Derivative sidedness'),

    #r0
    'r0_fixed': _('Fixed'),
    'r0_value': _('Value'),
    'r0_min': _('Minimum'),
    'r0_max': _('Maximum'),
    'r0_wrap': _('Wrap around'),
    'r0_step': _('Step'),
    'r0_relstep':_('Relative step'),
    'r0_side':_('Derivative sidedness'),

    #rt
    'rt_fixed': _('Fixed'),
    'rt_value': _('Value'),
    'rt_min': _('Minimum'),
    'rt_max': _('Maximum'),
    'rt_wrap': _('Wrap around'),
    'rt_step': _('Step'),
    'rt_relstep':_('Relative step'),
    'rt_side':_('Derivative sidedness'),

    #vt
    'vt_fixed': _('Fixed'),
    'vt_value': _('Value'),
    'vt_min': _('Minimum'),
    'vt_max': _('Maximum'),
    'vt_wrap': _('Wrap around'),
    'vt_step': _('Step'),
    'vt_relstep':_('Relative step'),
    'vt_side':_('Derivative sidedness'),
    
    #a
    'a_fixed': _('Fixed'),
    'a_value': _('Value'),
    'a_min': _('Minimum'),
    'a_max': _('Maximum'),
    'a_wrap': _('Wrap around'),
    'a_step': _('Step'),
    'a_relstep':_('Relative step'),
    'a_side':_('Derivative sidedness'),

    #b
    'b_fixed': _('Fixed'),
    'b_value': _('Value'),
    'b_min': _('Minimum'),
    'b_max': _('Maximum'),
    'b_wrap': _('Wrap around'),
    'b_step': _('Step'),
    'b_relstep':_('Relative step'),
    'b_side':_('Derivative sidedness'),
}

HELP_TEXTS = {
    # xo
    'xo_fixed': _(''),
    'xo_value': _(''),
    'xo_min': _(''),
    'xo_max': _(''),
    'xo_wrap': _('Is Wrap around parameter?'),
    'xo_step': _(''),
    'xo_relstep': _('Relative step size for finite difference.'),
    'xo_side': _('Sidedness of finite difference derivative.'),

    # yo
    'yo_fixed': _(''),
    'yo_value': _(''),
    'yo_min': _(''),
    'yo_max': _(''),
    'yo_wrap': _('Is Wrap around parameter?'),
    'yo_step': _(''),
    'yo_relstep': _('Relative step size for finite difference.'),
    'yo_side': _('Sidedness of finite difference derivative.'),

    # pa
    'pa_fixed': _(''),
    'pa_value': _(''),
    'pa_min': _(''),
    'pa_max': _(''),
    'pa_wrap': _('Is Wrap around parameter?'),
    'pa_step': _(''),
    'pa_relstep': _('Relative step size for finite difference.'),
    'pa_side': _('Sidedness of finite difference derivative.'),

    # incl
    'incl_fixed': _(''),
    'incl_value': _(''),
    'incl_min': _(''),
    'incl_max': _(''),
    'incl_wrap': _('Is Wrap around parameter?'),
    'incl_step': _(''),
    'incl_relstep': _('Relative step size for finite difference.'),
    'incl_side': _('Sidedness of finite difference derivative.'),

    # vsys
    'vsys_fixed': _(''),
    'vsys_value': _(''),
    'vsys_min': _(''),
    'vsys_max': _(''),
    'vsys_wrap': _('Is Wrap around parameter?'),
    'vsys_step': _(''),
    'vsys_relstep': _('Relative step size for finite difference.'),
    'vsys_side': _('Sidedness of finite difference derivative.'),

    # vsig
    'vsig_fixed': _(''),
    'vsig_value': _(''),
    'vsig_min': _(''),
    'vsig_max': _(''),
    'vsig_wrap': _('Is Wrap around parameter?'),
    'vsig_step': _(''),
    'vsig_relstep': _('Relative step size for finite difference.'),
    'vsig_side': _('Sidedness of finite difference derivative.'),

    'i0_fixed': _(''),
    'i0_value': _(''),
    'i0_min': _(''),
    'i0_max': _(''),
    'i0_wrap': _('Is Wrap around parameter?'),
    'i0_step': _(''),
    'i0_relstep': _('Relative step size for finite difference.'),
    'i0_side': _('Sidedness of finite difference derivative.'),

    # r0
    'r0_fixed': _(''),
    'r0_value': _(''),
    'r0_min': _(''),
    'r0_max': _(''),
    'r0_wrap': _('Is Wrap around parameter?'),
    'r0_step': _(''),
    'r0_relstep': _('Relative step size for finite difference.'),
    'r0_side': _('Sidedness of finite difference derivative.'),

    # rt
    'rt_fixed': _(''),
    'rt_value': _(''),
    'rt_min': _(''),
    'rt_max': _(''),
    'rt_wrap': _('Is Wrap around parameter?'),
    'rt_step': _(''),
    'rt_relstep': _('Relative step size for finite difference.'),
    'rt_side': _('Sidedness of finite difference derivative.'),

    # vt
    'vt_fixed': _(''),
    'vt_value': _(''),
    'vt_min': _(''),
    'vt_max': _(''),
    'vt_wrap': _('Is Wrap around parameter?'),
    'vt_step': _(''),
    'vt_relstep': _('Relative step size for finite difference.'),
    'vt_side': _('Sidedness of finite difference derivative.'),

    # a
    'a_fixed': _(''),
    'a_value': _(''),
    'a_min': _(''),
    'a_max': _(''),
    'a_wrap': _('Is Wrap around parameter?'),
    'a_step': _(''),
    'a_relstep': _('Relative step size for finite difference.'),
    'a_side': _('Sidedness of finite difference derivative.'),

    # b
    'b_fixed': _(''),
    'b_value': _(''),
    'b_min': _(''),
    'b_max': _(''),
    'b_wrap': _('Is Wrap around parameter?'),
    'b_step': _(''),
    'b_relstep': _('Relative step size for finite difference.'),
    'b_side': _('Sidedness of finite difference derivative.'),
}

class ParamsForm(forms.ModelForm):
    prefixes = ['xo', 'yo', 'pa', 'incl', 'vsys', 'vsig', 'i0', 'r0', 'rt', 'vt', 'a', 'b']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(ParamsForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'data-content': help_text, 'data-placement': 'top',
                     'data-container': 'body'})

    class Meta:
        model = ParameterSet
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
        help_texts = HELP_TEXTS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        ParameterSet.objects.create(
            job=job,

            xo_fixed=data.get('xo_fixed'),
            xo_value=data.get('xo_value'),
            xo_min=data.get('xo_min'),
            xo_max=data.get('xo_max'),
            xo_wrap=data.get('xo_wrap'),
            xo_step=data.get('xo_step'),
            xo_relstep=data.get('xo_relstep'),
            xo_side=data.get('xo_side'),

            yo_fixed=data.get('yo_fixed'),
            yo_value=data.get('yo_value'),
            yo_min=data.get('yo_min'),
            yo_max=data.get('yo_max'),
            yo_wrap=data.get('yo_wrap'),
            yo_step=data.get('yo_step'),
            yo_relstep=data.get('yo_relstep'),
            yo_side=data.get('yo_side'),

            pa_fixed=data.get('pa_fixed'),
            pa_value=data.get('pa_value'),
            pa_min=data.get('pa_min'),
            pa_max=data.get('pa_max'),
            pa_wrap=data.get('pa_wrap'),
            pa_step=data.get('pa_step'),
            pa_relstep=data.get('pa_relstep'),
            pa_side=data.get('pa_side'),

            incl_fixed=data.get('incl_fixed'),
            incl_value=data.get('incl_value'),
            incl_min=data.get('incl_min'),
            incl_max=data.get('incl_max'),
            incl_wrap=data.get('incl_wrap'),
            incl_step=data.get('incl_step'),
            incl_relstep=data.get('incl_relstep'),
            incl_side=data.get('incl_side'),

            vsys_fixed=data.get('vsys_fixed'),
            vsys_value=data.get('vsys_value'),
            vsys_min=data.get('vsys_min'),
            vsys_max=data.get('vsys_max'),
            vsys_wrap=data.get('vsys_wrap'),
            vsys_step=data.get('vsys_step'),
            vsys_relstep=data.get('vsys_relstep'),
            vsys_side=data.get('vsys_side'),

            vsig_fixed=data.get('vsig_fixed'),
            vsig_value=data.get('vsig_value'),
            vsig_min=data.get('vsig_min'),
            vsig_max=data.get('vsig_max'),
            vsig_wrap=data.get('vsig_wrap'),
            vsig_step=data.get('vsig_step'),
            vsig_relstep=data.get('vsig_relstep'),
            vsig_side=data.get('vsig_side'),

            i0_fixed=data.get('i0_fixed'),
            i0_value=data.get('i0_value'),
            i0_min=data.get('i0_min'),
            i0_max=data.get('i0_max'),
            i0_wrap=data.get('i0_wrap'),
            i0_step=data.get('i0_step'),
            i0_relstep=data.get('i0_relstep'),
            i0_side=data.get('i0_side'),

            r0_fixed=data.get('r0_fixed'),
            r0_value=data.get('r0_value'),
            r0_min=data.get('r0_min'),
            r0_max=data.get('r0_max'),
            r0_wrap=data.get('r0_wrap'),
            r0_step=data.get('r0_step'),
            r0_relstep=data.get('r0_relstep'),
            r0_side=data.get('r0_side'),

            rt_fixed=data.get('rt_fixed'),
            rt_value=data.get('rt_value'),
            rt_min=data.get('rt_min'),
            rt_max=data.get('rt_max'),
            rt_wrap=data.get('rt_wrap'),
            rt_step=data.get('rt_step'),
            rt_relstep=data.get('rt_relstep'),
            rt_side=data.get('rt_side'),

            vt_fixed=data.get('vt_fixed'),
            vt_value=data.get('vt_value'),
            vt_min=data.get('vt_min'),
            vt_max=data.get('vt_max'),
            vt_wrap=data.get('vt_wrap'),
            vt_step=data.get('vt_step'),
            vt_relstep=data.get('vt_relstep'),
            vt_side=data.get('vt_side'),

            a_fixed=data.get('a_fixed'),
            a_value=data.get('a_value'),
            a_min=data.get('a_min'),
            a_max=data.get('a_max'),
            a_wrap=data.get('a_wrap'),
            a_step=data.get('a_step'),
            a_relstep=data.get('a_relstep'),
            a_side=data.get('a_side'),

            b_fixed=data.get('b_fixed'),
            b_value=data.get('b_value'),
            b_min=data.get('b_min'),
            b_max=data.get('b_max'),
            b_wrap=data.get('b_wrap'),
            b_step=data.get('b_step'),
            b_relstep=data.get('b_relstep'),
            b_side=data.get('b_side'),
        )

        self.request.session['params'] = self.as_array(data)

    def as_array(self, data):
        return [self.i0_dict(data),
                self.r0_dict(data),
                self.xo_dict(data),
                self.yo_dict(data),
                self.pa_dict(data),
                self.incl_dict(data),
                self.rt_dict(data),
                self.vt_dict(data),
                self.vsys_dict(data),
                self.vsig_dict(data),
                self.a_dict(data),
                self.b_dict(data),
                ]

    def i0_dict(self, data):
        # i0
        i0_dict = {
            'name': 'i0'
        }
        try:
            i0_dict['fixed'] = data.get('i0_fixed')
        except:
            pass

        try:
            i0_dict['value'] = data.get('i0_value')
        except:
            pass

        try:
            i0_dict['min'] = data.get('i0_min')
        except:
            pass

        try:
            i0_dict['max'] = data.get('i0_max')
        except:
            pass
        try:
            i0_dict['wrap'] = data.get('i0_wrap')
        except:
            pass

        try:
            i0_dict['step'] = data.get('i0_step')
        except:
            pass

        try:
            i0_dict['relstep'] = data.get('i0_relstep')
        except:
            pass

        try:
            i0_dict['side'] = data.get('i0_side')
        except:
            pass

        try:
            i0_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            i0_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return i0_dict

    def r0_dict(self, data):
        # r0
        r0_dict = {
            'name': 'r0'
        }
        try:
            r0_dict['fixed'] = data.get('r0_fixed')
        except:
            pass

        try:
            r0_dict['value'] = data.get('r0_value')
        except:
            pass

        try:
            r0_dict['min'] = data.get('r0_min')
        except:
            pass

        try:
            r0_dict['max'] = data.get('r0_max')
        except:
            pass
        try:
            r0_dict['wrap'] = data.get('r0_wrap')
        except:
            pass

        try:
            r0_dict['step'] = data.get('r0_step')
        except:
            pass

        try:
            r0_dict['relstep'] = data.get('r0_relstep')
        except:
            pass

        try:
            r0_dict['side'] = data.get('r0_side')
        except:
            pass

        try:
            r0_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            r0_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return r0_dict

    def xo_dict(self, data):
        # xo
        xo_dict = {
            'name': 'xo'
        }
        try:
            xo_dict['fixed'] = data.get('xo_fixed')
        except:
            pass

        try:
            xo_dict['value'] = data.get('xo_value')
        except:
            pass

        try:
            xo_dict['min'] = data.get('xo_min')
        except:
            pass

        try:
            xo_dict['max'] = data.get('xo_max')
        except:
            pass
        try:
            xo_dict['wrap'] = data.get('xo_wrap')
        except:
            pass

        try:
            xo_dict['step'] = data.get('xo_step')
        except:
            pass

        try:
            xo_dict['relstep'] = data.get('xo_relstep')
        except:
            pass

        try:
            xo_dict['side'] = data.get('xo_side')
        except:
            pass

        try:
            xo_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            xo_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return xo_dict

    def yo_dict(self, data):
        # yo
        yo_dict = {
            'name': 'yo'
        }
        try:
            yo_dict['fixed'] = data.get('yo_fixed')
        except:
            pass

        try:
            yo_dict['value'] = data.get('yo_value')
        except:
            pass

        try:
            yo_dict['min'] = data.get('yo_min')
        except:
            pass

        try:
            yo_dict['max'] = data.get('yo_max')
        except:
            pass
        try:
            yo_dict['wrap'] = data.get('yo_wrap')
        except:
            pass

        try:
            yo_dict['step'] = data.get('yo_step')
        except:
            pass

        try:
            yo_dict['relstep'] = data.get('yo_relstep')
        except:
            pass

        try:
            yo_dict['side'] = data.get('yo_side')
        except:
            pass

        try:
            yo_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            yo_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return yo_dict

    def pa_dict(self, data):
        # pa
        pa_dict = {
            'name': 'pa'
        }
        try:
            pa_dict['fixed'] = data.get('pa_fixed')
        except:
            pass

        try:
            pa_dict['value'] = data.get('pa_value')
        except:
            pass

        try:
            pa_dict['min'] = data.get('pa_min')
        except:
            pass

        try:
            pa_dict['max'] = data.get('pa_max')
        except:
            pass
        try:
            pa_dict['wrap'] = data.get('pa_wrap')
        except:
            pass

        try:
            pa_dict['step'] = data.get('pa_step')
        except:
            pass

        try:
            pa_dict['relstep'] = data.get('pa_relstep')
        except:
            pass

        try:
            pa_dict['side'] = data.get('pa_side')
        except:
            pass

        try:
            pa_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            pa_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return pa_dict

    def incl_dict(self, data):
        # incl
        incl_dict = {
            'name': 'incl'
        }
        try:
            incl_dict['fixed'] = data.get('incl_fixed')
        except:
            pass

        try:
            incl_dict['value'] = data.get('incl_value')
        except:
            pass

        try:
            incl_dict['min'] = data.get('incl_min')
        except:
            pass

        try:
            incl_dict['max'] = data.get('incl_max')
        except:
            pass
        try:
            incl_dict['wrap'] = data.get('incl_wrap')
        except:
            pass

        try:
            incl_dict['step'] = data.get('incl_step')
        except:
            pass

        try:
            incl_dict['relstep'] = data.get('incl_relstep')
        except:
            pass

        try:
            incl_dict['side'] = data.get('incl_side')
        except:
            pass

        try:
            incl_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            incl_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return incl_dict

    def rt_dict(self, data):
        # rt
        rt_dict = {
            'name': 'rt'
        }
        try:
            rt_dict['fixed'] = data.get('rt_fixed')
        except:
            pass

        try:
            rt_dict['value'] = data.get('rt_value')
        except:
            pass

        try:
            rt_dict['min'] = data.get('rt_min')
        except:
            pass

        try:
            rt_dict['max'] = data.get('rt_max')
        except:
            pass
        try:
            rt_dict['wrap'] = data.get('rt_wrap')
        except:
            pass

        try:
            rt_dict['step'] = data.get('rt_step')
        except:
            pass

        try:
            rt_dict['relstep'] = data.get('rt_relstep')
        except:
            pass

        try:
            rt_dict['side'] = data.get('rt_side')
        except:
            pass

        try:
            rt_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            rt_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return rt_dict

    def vt_dict(self, data):
        # vt
        vt_dict = {
            'name': 'vt'
        }
        try:
            vt_dict['fixed'] = data.get('vt_fixed')
        except:
            pass

        try:
            vt_dict['value'] = data.get('vt_value')
        except:
            pass

        try:
            vt_dict['min'] = data.get('vt_min')
        except:
            pass

        try:
            vt_dict['max'] = data.get('vt_max')
        except:
            pass
        try:
            vt_dict['wrap'] = data.get('vt_wrap')
        except:
            pass

        try:
            vt_dict['step'] = data.get('vt_step')
        except:
            pass

        try:
            vt_dict['relstep'] = data.get('vt_relstep')
        except:
            pass

        try:
            vt_dict['side'] = data.get('vt_side')
        except:
            pass

        try:
            vt_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            vt_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return vt_dict

    def vsys_dict(self, data):
        # vsys
        vsys_dict = {
            'name': 'vsys'
        }
        try:
            vsys_dict['fixed'] = data.get('vsys_fixed')
        except:
            pass

        try:
            vsys_dict['value'] = data.get('vsys_value')
        except:
            pass

        try:
            vsys_dict['min'] = data.get('vsys_min')
        except:
            pass

        try:
            vsys_dict['max'] = data.get('vsys_max')
        except:
            pass
        try:
            vsys_dict['wrap'] = data.get('vsys_wrap')
        except:
            pass

        try:
            vsys_dict['step'] = data.get('vsys_step')
        except:
            pass

        try:
            vsys_dict['relstep'] = data.get('vsys_relstep')
        except:
            pass

        try:
            vsys_dict['side'] = data.get('vsys_side')
        except:
            pass

        try:
            vsys_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            vsys_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return vsys_dict

    def vsig_dict(self, data):
        # vsig
        vsig_dict = {
            'name': 'vsig'
        }
        try:
            vsig_dict['fixed'] = data.get('vsig_fixed')
        except:
            pass

        try:
            vsig_dict['value'] = data.get('vsig_value')
        except:
            pass

        try:
            vsig_dict['min'] = data.get('vsig_min')
        except:
            pass

        try:
            vsig_dict['max'] = data.get('vsig_max')
        except:
            pass
        try:
            vsig_dict['wrap'] = data.get('vsig_wrap')
        except:
            pass

        try:
            vsig_dict['step'] = data.get('vsig_step')
        except:
            pass

        try:
            vsig_dict['relstep'] = data.get('vsig_relstep')
        except:
            pass

        try:
            vsig_dict['side'] = data.get('vsig_side')
        except:
            pass

        try:
            vsig_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            vsig_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return vsig_dict
    
    def a_dict(self, data):
        # a
        a_dict = {
            'name': 'a'
        }
        try:
            a_dict['fixed'] = data.get('a_fixed')
        except:
            pass

        try:
            a_dict['value'] = data.get('a_value')
        except:
            pass

        try:
            a_dict['min'] = data.get('a_min')
        except:
            pass

        try:
            a_dict['max'] = data.get('a_max')
        except:
            pass
        try:
            a_dict['wrap'] = data.get('a_wrap')
        except:
            pass

        try:
            a_dict['step'] = data.get('a_step')
        except:
            pass

        try:
            a_dict['relstep'] = data.get('a_relstep')
        except:
            pass

        try:
            a_dict['side'] = data.get('a_side')
        except:
            pass

        try:
            a_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            a_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return a_dict

    def b_dict(self, data):
        # b
        b_dict = {
            'name': 'b'
        }
        try:
            b_dict['fixed'] = data.get('b_fixed')
        except:
            pass

        try:
            b_dict['value'] = data.get('b_value')
        except:
            pass

        try:
            b_dict['min'] = data.get('b_min')
        except:
            pass

        try:
            b_dict['max'] = data.get('b_max')
        except:
            pass
        try:
            b_dict['wrap'] = data.get('b_wrap')
        except:
            pass

        try:
            b_dict['step'] = data.get('b_step')
        except:
            pass

        try:
            b_dict['relstep'] = data.get('b_relstep')
        except:
            pass

        try:
            b_dict['side'] = data.get('b_side')
        except:
            pass

        try:
            b_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            b_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        return b_dict

class EditParamsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        vel_profile = None
        fitter_type = None

        if self.job_id:
            try:
                self.request.session['params'] = ParameterSet.objects.get(job_id=self.job_id).as_array()
            except:
                pass

            try:
                vel_profile = GalaxyModel.objects.get(job_id=self.job_id).vel_profile
            except:
                pass

            try:
                fitter_type = Fitter.objects.get(job_id=self.job_id).fitter_type
            except:
                pass

        super(EditParamsForm, self).__init__(*args, **kwargs)

        # Add help_text to html/css
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'data-content': help_text, 'data-placement': 'top',
                     'data-container': 'body'})

        if vel_profile != None:
            if vel_profile != GalaxyModel.EPINAT:
                for field in A_FIELDS:
                    if field in self.fields: del self.fields[field]
                for field in B_FIELDS:
                    if field in self.fields: del self.fields[field]

        if fitter_type != None:
            if fitter_type == Fitter.MPFIT:
                """
                Uses:
                    - fixed 
                    - value 
                    - min 
                    - max 
                    - step 
                    - relstep 
                    - side
                
                Doesn't use:
                    - wrap
                """
                for fields_list in FIELDS_LISTS:
                    for field in fields_list:
                        if 'wrap' in field:
                            if field in self.fields: del self.fields[field]

            if fitter_type == Fitter.MULTINEST:
                """
                Uses:
                    - fixed
                    - min
                    - max
                    - wrap
                    - value
                Doesn't use:
                    - step 
                    - relstep 
                    - side
                """
                for fields_list in FIELDS_LISTS:
                    for field in fields_list:
                        if 'step' in field or 'relstep' in field or 'side' in field:
                            if field in self.fields: del self.fields[field]

    class Meta:
        model = ParameterSet
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
        help_texts = HELP_TEXTS


