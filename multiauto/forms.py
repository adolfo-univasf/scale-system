from django import forms
from django.shortcuts import get_object_or_404
from django.template import loader,Template, Context
from django.forms.utils import ErrorList
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from functools import reduce

class EdiTableForm(forms.ModelForm):
    ID = 0
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None, edit=True, add=False, parent=None, field=None):
        self.editable = edit
        self.addable = add
        self.parent = parent
        self.field = field
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=None, error_class=error_class, label_suffix=label_suffix,
                         empty_permitted=empty_permitted, instance=None, use_required_attribute=use_required_attribute, renderer=renderer)
        self.id = 'editable'+str(EdiTableForm.ID)
        self.cls = type(self.instance)
        EdiTableForm.ID += 1
        if data:
            self.multivalues = []
            tempdata = {}
            tempdata['pk'] = data['pk'].split(" # ")
            for field in self.fields.items():
                tempdata[field[0]] = data[field[0]].split(" # ")
            for i in range(len(tempdata['pk'])):
                row = {'pk':tempdata['pk'][i], 'fields':[]}
                for field in self.fields.items():
                    fields = {}
                    fields['instance'] = field[1]
                    if isinstance(field[1],ModelMultipleChoiceField):
                        fields['value'] = tempdata[field[0]][i]
                        fields['data'] = []
                        fields['html'] = ""
                        for pk in fields['value'].split(", "):
                            if not pk:
                                pass
                            elif pk[:1] !='$':
                                d = get_object_or_404(field[1].queryset.model, pk=int(pk))
                                fields['data'].append(d)
                                fields['html'] = str(d)+", "
                            else:
                                help = field[1].help_text.split('|')
                                d = tempdata[help[2]][int(fields['value'][1:])]+", "
                                fields['html'] = str(d)+", "
                                fields['data'].append(pk)


                    elif isinstance(field[1],ModelChoiceField):
                        fields['value'] = tempdata[field[0]][i]
                        if not fields['value']:
                            fields['data'] = None
                            fields['html'] = ""
                        elif fields['value'][:1] != "$":
                            fields['data'] = field[1].queryset.model.objects.get(pk=int(fields['value']))
                            fields['html'] = str(fields['data'])
                        elif(field[1].help_text):
                            help = field[1].help_text.split('|')
                            fields['html'] = tempdata[help[2]][int(fields['value'][1:])]
                    else:
                        fields['html'] = tempdata[field[0]][i]
                        fields['value'] = ""
                        fields['data'] = tempdata[field[0]][i]
                    fields['name'] = field[0]
                    fields['label'] = field[1].label
                    fields['editable'] = False
                    fields['type'] = 'text'
                    if(field[1].help_text):
                        help = field[1].help_text.split('|')
                        fields['editable'] = True
                        fields['type'] = help[0]
                        if help[0]=='select' or help[0]=='multiauto':
                            if(help[1]=='url'):
                                fields['url'] = help[2]
                            elif (help[1]=='func'):
                                fields['func'] = "relatedEdiTable(.{},{})".format(self.id, help[2])
                            elif(help[1]=='obj'):
                                fields['obj'] = help[2]
                    row['fields'].append(fields)
                self.multivalues.append(row)


        elif instance:
            def m(data):
                row = {}
                row['pk'] = data.pk
                row['fields'] = []
                for field in self.fields.items():
                    fields = {}
                    fields['instance'] = field[1]
                    if isinstance(field[1],ModelMultipleChoiceField):
                        value = getattr(data, field[0])
                        value = list(value.get_queryset())
                        fields['data'] = value
                        if value:
                            fields['value']=reduce(lambda a,d: a+d,map(lambda d: str(d.pk)+", ",value))
                            fields['html']=reduce(lambda a,d: a+d,map(lambda d: str(d)+", ",value))
                        else:
                            fields['html']=""
                            fields['value'] = ""
                    elif isinstance(field[1],ModelChoiceField):
                        value = getattr(data, field[0])
                        fields['data'] = value
                        if value:
                            fields['value']=value.pk
                            fields['html']=str(getattr(data, field[0]))
                        else:
                            fields['value']=""
                            fields['html']=""
                    else:
                        fields['html']= getattr(data, field[0])
                        fields['value'] = ""
                        fields['data'] = fields['html']
                    if fields['html'] is None:
                        fields['html'] = ""
                    
                    fields['name'] = field[0]
                    fields['label'] = field[1].label
                    fields['editable'] = False
                    fields['type'] = 'text'
                    if(field[1].help_text):
                        help = field[1].help_text.split('|')
                        fields['editable'] = True
                        fields['type'] = help[0]
                        if help[0]=='select' or help[0]=='multiauto':
                            if(help[1]=='url'):
                                fields['url'] = help[2]
                            elif (help[1]=='func'):
                                fields['func'] = "relatedEdiTable(.{},{})".format(self.id, help[2])
                            elif(help[1]=='obj'):
                                fields['obj'] = help[2]
                    row['fields'].append(fields)
                return row
            self.multivalues = list(map(m,list(instance)))
        else:
            self.multivalues = False
        

    class Media:
        css = {'all': ('multiauto/css/jquery-ui.css',
                       "multiauto/css/estilo.css")}
        js = ('multiauto/js/jquery-1.12.4.js',
              'multiauto/js/jquery-ui.js',
              'multiauto/js/multiauto.js',
              'multiauto/js/editable.js')

    def as_table(self):
        template_name = "multiauto/editable.html"
        context = {}
        context['id'] = self.id
        context['editable'] = self.editable
        context['addable'] = self.addable
        context['fields'] = []
        for field in self.fields.items():
            fields = {}
            fields['name'] = field[0]
            fields['label'] = field[1].label
            fields['editable'] = True
            fields['type'] = 'text'
            if(field[1].help_text):
                help = field[1].help_text.split('|')
                fields['type'] = help[0]
                if help[0]=='select' or help[0]=='multiauto':
                    if(help[1]=='url'):
                        fields['url'] = help[2]
                    elif (help[1]=='func'):
                            fields['func'] = "relatedEdiTable(.{},{})".format(self.id, help[2])
                    elif(help[1]=='obj'):
                        fields['obj'] = help[2]
            context['fields'].append(fields)
        
        if self.multivalues:
            context['instance'] = self.multivalues
        return loader.render_to_string(template_name, context)

    def save(self):
        if self.multivalues:
            models = []
            for mv in self.multivalues:
                md = self.cls() if mv['pk'] is None or mv['pk'] == "" else get_object_or_404(self.cls,pk=mv['pk'])
                for field in mv['fields']:
                    print(field['instance'])
                    if not isinstance(field['instance'],ModelMultipleChoiceField) and not isinstance(field['instance'],ModelChoiceField):
                        if field['data']=="":
                            setattr(md, field['name'], None)    
                        else:
                            setattr(md, field['name'], field['data'])
                if self.parent and self.field:
                    setattr(md, self.field, self.parent)
                md.save()
                models.append(md)
            for i,mv in enumerate(self.multivalues):
                md = models[i]
                for field in mv['fields']:
                    if isinstance(field['instance'],ModelMultipleChoiceField):
                        values = field['data']
                        for i,vl in enumerate(values):
                            if type(vl) == str:
                                vl = models[int(vl[1:])]#TODO find elements multiauto
                            values[i] = vl
                        old = list(getattr(md,field['name']).get_queryset())

                        # adiciona os novos
                        for vl in values:
                            if vl not in old:
                                getattr(md,field['name']).add(vl)
                        # adiciona os novos
                        for vl in old:
                            if vl not in values:
                                getattr(md,field['name']).remove(vl)

                    elif isinstance(field['instance'],ModelChoiceField):
                        if not field['value']:
                            setattr(md, field['name'], None)
                        elif field['value'][:1] != "$":
                            setattr(md, field['name'], field['instance'].queryset.model.objects.get(pk=int(field['value'])))
                        else:
                            setattr(md, field['name'], models[int(field['value'][1:])])
                md.save()
            if self.parent and self.field:
                filter_dict = {}
                filter_dict[self.field]=self.parent
                old = list(self.cls.objects.filter(**filter_dict))
                for vl in old:
                    if vl not in models:
                        vl.delete()
            return models


"""
from programs.models import Program, ProgramTime
from programs.forms import ProgramTimeForm
program = Program.objects.all()[0]
pt = ProgramTime.objects.filter(program = program)
form = ProgramTimeForm(instance = pt)
str(form)

"""
