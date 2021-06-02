from django import forms
from .models import Program
from django.utils.translation import gettext as _


class ProgramRegisterForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'date', 'transmission', 'room',
                  'presential', 'iscription', 'image', 'description']

class UseTemplateForm(forms.Form):
    templates = forms.ModelChoiceField(
        queryset=Program.objects.filter(date__isnull=True), 
        empty_label=_("select a template..."))