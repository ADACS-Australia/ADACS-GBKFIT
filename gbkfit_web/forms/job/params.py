from django import forms
from django.utils.translation import ugettext_lazy as _
from gbkfit_web.models import ParameterSet, Job

FIELDS = [
            #i0
            'i0_fixed',
            'i0_value',
            'i0_min',
            'i0_max',
            'i0_wrap',
            'i0_step',
            'i0_relstep',
            'i0_side',

            #r0
            'r0_fixed',
            'r0_value',
            'r0_min',
            'r0_max',
            'r0_wrap',
            'r0_step',
            'r0_relstep',
            'r0_side',

            #xo
            'xo_fixed',
            'xo_value',
            'xo_min',
            'xo_max',
            'xo_wrap',
            'xo_step',
            'xo_relstep',
            'xo_side',

            #yo
            'yo_fixed',
            'yo_value',
            'yo_min',
            'yo_max',
            'yo_wrap',
            'yo_step',
            'yo_relstep',
            'yo_side',

            #pa
            'pa_fixed',
            'pa_value',
            'pa_min',
            'pa_max',
            'pa_wrap',
            'pa_step',
            'pa_relstep',
            'pa_side',

            #incl
            'incl_fixed',
            'incl_value',
            'incl_min',
            'incl_max',
            'incl_wrap',
            'incl_step',
            'incl_relstep',
            'incl_side',

            #rt
            'rt_fixed',
            'rt_value',
            'rt_min',
            'rt_max',
            'rt_wrap',
            'rt_step',
            'rt_relstep',
            'rt_side',

            #vt
            'vt_fixed',
            'vt_value',
            'vt_min',
            'vt_max',
            'vt_wrap',
            'vt_step',
            'vt_relstep',
            'vt_side',

            #vsys
            'vsys_fixed',
            'vsys_value',
            'vsys_min',
            'vsys_max',
            'vsys_wrap',
            'vsys_step',
            'vsys_relstep',
            'vsys_side',

            #vsig
            'vsig_fixed',
            'vsig_value',
            'vsig_min',
            'vsig_max',
            'vsig_wrap',
            'vsig_step',
            'vsig_relstep',
            'vsig_side',
        ]

WIDGETS= {
            'i0_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'i0_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # r0
            'r0_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'r0_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # xo
            'xo_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xo_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # yo
            'yo_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'yo_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # pa
            'pa_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'pa_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # incl
            'incl_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'incl_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # rt
            'rt_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'rt_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # vt
            'vt_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vt_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # vsys
            'vsys_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsys_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),

            # vsig
            'vsig_fixed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_value': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_min': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_max': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_wrap': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_step': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_relstep': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'vsig_side': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }

LABELS = {
    'i0_fixed': _('Fixed'),
    'i0_value': _('Value'),
    'i0_min': _('Minimum'),
    'i0_max': _('Maximum'),
    'i0_wrap': _('Wrap'),
    'i0_step': _('Step'),
    'i0_relstep': _('Relstep'),
    'i0_side': _('Side'),

    #r0
    'r0_fixed': _('Fixed'),
    'r0_value': _('Value'),
    'r0_min': _('Minimum'),
    'r0_max': _('Maximum'),
    'r0_wrap': _('Wrap'),
    'r0_step': _('Step'),
    'r0_relstep': _('Relstep'),
    'r0_side': _('Side'),

    #xo
    'xo_fixed': _('Fixed'),
    'xo_value': _('Value'),
    'xo_min': _('Minimum'),
    'xo_max': _('Maximum'),
    'xo_wrap': _('Wrap'),
    'xo_step': _('Step'),
    'xo_relstep': _('Relstep'),
    'xo_side': _('Side'),

    #yo
    'yo_fixed': _('Fixed'),
    'yo_value': _('Value'),
    'yo_min': _('Minimum'),
    'yo_max': _('Maximum'),
    'yo_wrap': _('Wrap'),
    'yo_step': _('Step'),
    'yo_relstep': _('Relstep'),
    'yo_side': _('Side'),

    #pa
    'pa_fixed': _('Fixed'),
    'pa_value': _('Value'),
    'pa_min': _('Minimum'),
    'pa_max': _('Maximum'),
    'pa_wrap': _('Wrap'),
    'pa_step': _('Step'),
    'pa_relstep': _('Relstep'),
    'pa_side': _('Side'),

    #incl
    'incl_fixed': _('Fixed'),
    'incl_value': _('Value'),
    'incl_min': _('Minimum'),
    'incl_max': _('Maximum'),
    'incl_wrap': _('Wrap'),
    'incl_step': _('Step'),
    'incl_relstep': _('Relstep'),
    'incl_side': _('Side'),

    #rt
    'rt_fixed': _('Fixed'),
    'rt_value': _('Value'),
    'rt_min': _('Minimum'),
    'rt_max': _('Maximum'),
    'rt_wrap': _('Wrap'),
    'rt_step': _('Step'),
    'rt_relstep': _('Relstep'),
    'rt_side': _('Side'),

    #vt
    'vt_fixed': _('Fixed'),
    'vt_value': _('Value'),
    'vt_min': _('Minimum'),
    'vt_max': _('Maximum'),
    'vt_wrap': _('Wrap'),
    'vt_step': _('Step'),
    'vt_relstep': _('Relstep'),
    'vt_side': _('Side'),

    #vsys
    'vsys_fixed': _('Fixed'),
    'vsys_value': _('Value'),
    'vsys_min': _('Minimum'),
    'vsys_max': _('Maximum'),
    'vsys_wrap': _('Wrap'),
    'vsys_step': _('Step'),
    'vsys_relstep': _('Relstep'),
    'vsys_side': _('Side'),

    #vsig
    'vsig_fixed': _('Fixed'),
    'vsig_value': _('Value'),
    'vsig_min': _('Minimum'),
    'vsig_max': _('Maximum'),
    'vsig_wrap': _('Wrap'),
    'vsig_step': _('Step'),
    'vsig_relstep': _('Relstep'),
    'vsig_side': _('Side'),
}

class ParamsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ParamsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ParameterSet
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS


    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            result = ParameterSet.objects.create(
                job=job,

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
            )
        except:
            result = ParameterSet.objects.filter(job_id=id).update(
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
            )

        self.request.session['params'] = ParameterSet.objects.get(job_id=id).as_array()

class EditParamsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditParamsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ParameterSet
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

