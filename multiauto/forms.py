from django import forms
from django.template import loader,Template, Context
from django.forms.utils import ErrorList
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from functools import reduce

class EdiTableForm(forms.ModelForm):
    ID = 0
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=None, error_class=error_class, label_suffix=label_suffix,
                         empty_permitted=empty_permitted, instance=None, use_required_attribute=use_required_attribute, renderer=renderer)
        self.id = 'editable'+str(EdiTableForm.ID)
        self.cls = type(self.instance)
        EdiTableForm.ID += 1
        if data:
            self.multivalues = []
            print('------------------------------------------------')
            tempdata = {}
            tempdata['pk'] = data['pk'].split(" # ")
            for field in self.fields.items():
                tempdata[field[0]] = data[field[0]].split(" # ")
            for i in range(len(tempdata['pk'])):
                row = {'pk':tempdata['pk'][i], 'fields':[]}
                for field in self.fields.items():
                    fields = {}
                    if isinstance(field[1],ModelMultipleChoiceField):
                        fields['html'] = tempdata[field[0]][i]
                        fields['value'] = ""
                        fields['data'] = fields['html'].split(", ")
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
                                if help[0]=='select':
                                    fields['func'] = "related_selectEdiTable(.{},{})".format(self.id, help[2])
                                else:
                                    fields['func'] = "relatedEdiTable(.{},{})".format(self.id, help[2])
                            elif(help[1]=='obj'):
                                fields['obj'] = help[2]
                    row['fields'].append(fields)
                self.multivalues.append(row)
            print('------------------------------------------------')


        elif instance:
            def m(data):
                row = {}
                row['pk'] = data.pk
                row['fields'] = []
                for field in self.fields.items():
                    fields = {}
                    if isinstance(field[1],ModelMultipleChoiceField):
                        value = getattr(data, field[0])
                        value = list(value.get_queryset())
                        fields['html']=reduce(lambda a,d: a+d,map(lambda d: str(d)+", ",value))
                        fields['value'] = ""
                        fields['data'] = value
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
                                if help[0]=='select':
                                    fields['func'] = "related_selectEdiTable(.{},{})".format(self.id, help[2])
                                else:
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
                        if help[0]=='select':
                            fields['func'] = "related_selectEdiTable(.{},{})".format(self.id, help[2])
                        else:
                            fields['func'] = "relatedEdiTable(.{},{})".format(self.id, help[2])
                    elif(help[1]=='obj'):
                        fields['obj'] = help[2]
            context['fields'].append(fields)
        
        if self.multivalues:
            context['instance'] = self.multivalues
        return loader.render_to_string(template_name, context)

    def save(self, program):
        pass


"""
from programs.models import Program, ProgramTime
from programs.forms import ProgramTimeForm
program = Program.objects.all()[0]
pt = ProgramTime.objects.filter(program = program)
form = ProgramTimeForm(instance = pt)
str(form)

"""
