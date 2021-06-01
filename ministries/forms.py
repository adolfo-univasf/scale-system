from django import forms
from multiauto.widgets import MultiAutoComplete
from .models import Ministry, Function
from accounts.models import User

class MinistryRegisterForm(forms.ModelForm):
    leader = forms.CharField(widget = MultiAutoComplete,required=False)

    def __init__(self, *args, options = [],leader_value = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.declared_fields['leader'].widget.options = options
        try:
            leader_value = leader_value if leader_value else kwargs['instance'].get_leader_string()
        except KeyError as identifier:
            pass
            
        self.declared_fields['leader'].widget.value = leader_value
    def set_options(self, options):
        self.declared_fields['leader'].widget.options = options

    def save(self, commit=True):
        ministry = super(MinistryRegisterForm, self).save()
        ld = self.data['leader']
        ld = ld.split(', ')
        ld = filter(lambda x : len(x)>0,ld)
        for i in ld:
            if i is not None and i != "":
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


class FunctionRegisterForm(forms.ModelForm):
    people = forms.CharField(widget = MultiAutoComplete,required=False)
    overload = forms.CharField(widget = MultiAutoComplete,required=False)

    def __init__(self,*args,ministry = None, options = [],options2 = [],people_value = "",overload_value = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.declared_fields['people'].widget.options = options
        self.declared_fields['overload'].widget.options2 = options
        try:
            people_value = people_value if people_value else kwargs['instance'].get_people_string()
            overload_value = overload_value if overload_value else kwargs['instance'].get_overload_string()
        except KeyError as identifier:
            pass            
        self.declared_fields['people'].widget.value = people_value
        self.declared_fields['overload'].widget.value = overload_value
        self.ministry = ministry
    def set_options(self, options_people=None, options_overload=None):
        if options_people:
            self.declared_fields['people'].widget.options = options_people
        if options_overload:
            self.declared_fields['overload'].widget.options = options_overload
        

    def save(self, commit=True):
        function = super(FunctionRegisterForm, self).save(commit=False)
        function.ministry = self.ministry
        function.save()
        po = self.data['people']
        po = po.split(', ')
        po = filter(lambda x : len(x)>0,po)
        for i in po:
            if i is not None and i != "":
                us = User.get_user_by_name(i)
                if us.pk is None :
                    us.save()
                function.people.add(us)
        fn = self.data['overload']
        fn = fn.split(', ')
        fn = filter(lambda x : len(x)>0,fn)
        for i in fn:
            if i is not None and i != "":
                fn = Function.objects.filter(name__contains = i).first()
                if fn:
                    function.overload.add(fn)

        if commit:
            function.save()
        return function

    class Meta:
        model = Function
        fields = ['name']