from django import forms
from programs.models import ProgramTime
from multiauto.forms import EdiTableForm

class EditPersonForm(EdiTableForm):
    class Meta:
        model = ProgramTime
        fields = ['program', 'person']
        help_texts = {'person': 'multiauto|url|/accounts/all'}