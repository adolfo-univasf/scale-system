from django import forms
from django.shortcuts import get_object_or_404
from multiauto.widgets import MultiAutoComplete
from .models import Ministry, Function
from accounts.models import User
from django.conf import settings

class MinistryRegisterForm(forms.ModelForm):
    leader = forms.CharField(widget = MultiAutoComplete,required=False)

    def __init__(self, *args, options = [],leader_value = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.declared_fields['leader'].widget.options = options
        try:
            if len(args)>0:
                leader_value = args[0]['leader_value']
            else:
                leader_value = leader_value if leader_value else kwargs['instance'].get_leader_string()
        except KeyError as identifier:
            pass
            
        self.widget_leader_value = leader_value
    def set_options(self, options):
        self.declared_fields['leader'].widget.options = options
        self.declared_fields['leader'].widget.value = self.widget_leader_value

    def save(self, commit=True):
        ministry = super(MinistryRegisterForm, self).save()
        ld = self.data['leader']
        ldv = self.data['leader_value']
        ld = ld.split(', ')
        ldv = ldv.split(', ')
        ld = [{'key':l,'value':v} for l,v in zip(ld,ldv)]
        for i in ld:
            if i is not None and i['value'] != "":
                us = User() if i['key']=="" else get_object_or_404(User, pk=int(i["key"]))
                if us.pk is None :
                    us.name = i['value']
                    lu = User.objects.all().order_by('-date_joined').first()
                    us.username = settings.DEFAULT_USERNAME +str(lu.pk+1)
                    us.email = settings.DEFAULT_USERNAME+str(lu.pk+1) + "@scale.br"
                    us.set_password(settings.DEFAULT_PASSWORD)
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
        pov = self.data['people_value']
        po = po.split(', ')
        pov = pov.split(', ')
        po = [{'key':l,'value':v} for l,v in zip(po,pov)]
        for i in po:
            if i is not None and i['value'] != "":
                us = User() if i['key']=="" else get_object_or_404(User, pk=int(i["key"]))
                if us.pk is None :
                    us.name = i['value']
                    lu = User.objects.all().order_by('-date_joined').first()
                    us.username = settings.DEFAULT_USERNAME +str(lu.pk+1)
                    us.email = settings.DEFAULT_USERNAME+str(lu.pk+1) + "@scale.br"
                    us.set_password(settings.DEFAULT_PASSWORD)
                    us.save()
                function.people.add(us)
        
        fn = self.data['overload']
        fnv = self.data['overload_value']
        fn = fn.split(', ')
        fnv = fnv.split(', ')
        fn = [{'ley':l,'value':v} for l,v in zip(fn,fnv)]
        for i in fn:
            if i is not None and i['value'] != "":
                fn = get_object_or_404(Function, pk=int(i["key"]))
                if fn:
                    function.overload.add(fn)

        if commit:
            function.save()
        return function

    class Meta:
        model = Function
        fields = ['name']