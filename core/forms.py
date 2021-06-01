from django import forms
from django.utils.translation import gettext as _
class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(label=_("You have shure?"))