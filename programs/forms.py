from django import forms
from .models import Program
from django.utils.translation import gettext as _
#from django.urls import reverse
from programs.models import ProgramTime
from multiauto.forms import EdiTableForm
from .utils import loopverify


class ProgramRegisterForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name','type_name', 'date', 'transmission', 'room',
                  'presential', 'iscription', 'image', 'description']


class UseTemplateForm(forms.Form):
    templates = forms.ModelChoiceField(
        queryset=Program.objects.filter(date__isnull=True),
        empty_label=_("select a template..."))


class ProgramTimeForm(EdiTableForm):
    def save(self):
        ret = super().save()
        loopverify(ret)
        return ret

    class Meta:
        model = ProgramTime
        fields = ['time', 'desc', 'function', 'lookup']
        help_texts = {'time':'text', 'desc':'text',
            'function': 'select|url|' +
                   '/ministries/allfunctionsselect', 'lookup': 'select|func|desc'}

class EditPersonForm(EdiTableForm):
    class Meta:
        model = ProgramTime
        fields = ['time', 'desc', 'person']
        help_texts = {'person': 'multiauto|url|/accounts/all'}