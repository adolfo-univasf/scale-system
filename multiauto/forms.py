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
        self.multivalues = instance
        self.id = 'editable-'+str(EdiTableForm.ID)
        EdiTableForm.ID += 1

    class Media:
        css = {'all': ('multiauto/css/jquery-ui.css',
                       "multiauto/css/estilo.css")}
        js = ('multiauto/js/jquery-1.12.4.js',
              'multiauto/js/jquery-ui.js',
              'multiauto/js/multiauto.js',
              'multiauto/js/js/editable.js')

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
                        fields['func'] = "relatedEdiTable(.{},{})".format(self.id, help[2])
                    elif(help[1]=='obj'):
                        fields['obj'] = help[2]
            context['fields'].append(fields)
        
        if self.multivalues:
            context['instance'] = []
            for multi in self.multivalues:
                instance = []
                for field in self.fields.items():
                    fields = {}
                    if isinstance(field[1],ModelMultipleChoiceField):
                        fields['html']=reduce(lambda a,d: a+d,map(lambda d: str(d)+", ",list(multi.getattr(object, field[0]).get_queryset())))
                        fields['value'] = ""
                    elif isinstance(field[1],ModelChoiceField):
                        fields['value']=multi.getattr(object, field[0]).pk
                        fields['html']=str(multi.getattr(object, field[0]))
                    else:
                        fields['html']=self.multivalues.getattr(object, field[0])
                        fields['value'] = ""
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
                    instance.append(fields)

                    
                context['instance'].append(instance)

        return loader.render_to_string(template_name, context)

    def save(self, program):
        pass


"""
from multiauto.forms import ProgramTimeForm
form = ProgramTimeForm()
str(form)

"""
