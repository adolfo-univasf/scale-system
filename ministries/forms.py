from django import forms
from multiauto.widgets import MultiAutoComplete
from .models import Ministry
from accounts.models import User

class MinistryRegisterForm(forms.ModelForm):
    leader = forms.CharField(widget = MultiAutoComplete,required=False)

    def __init__(self, *args, options = [],leader_value = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.declared_fields['leader'].widget.options = options
        self.declared_fields['leader'].widget.value = leader_value
    def set_options(self, options):
        self.declared_fields['leader'].widget.options = options

    def save(self, commit=True):
        ministry = super(MinistryRegisterForm, self).save()
        print(self.data['leader'])
        ld = self.data['leader'][0]
        ld = ld.split(', ')
        for i in ld:
            if i is not None or i != "":
                us = User.get_user_by_name(i)
                if us.pk is None :
                    us.save()
                ministry.leader.add(us)

        if commit:
            ministry.save()
        return ministry

    class Meta:
        model = Ministry
        fields = ['name', 'slug', 'code']