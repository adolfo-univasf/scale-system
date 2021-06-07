from django.forms import widgets

class MultiAutoComplete(widgets.TextInput):
    ID = 0
    template_name = 'multiauto/multiauto.html'
    class Media:
        css = {'all':('multiauto/css/jquery-ui.css',)}
        js = ('multiauto/js/jquery-1.12.4.js',
                'multiauto/js/jquery-ui.js',
                'multiauto/js/multiauto.js')
    def __init__(self,attrs={}, options=[], value = ""):
        self.id = MultiAutoComplete.ID
        MultiAutoComplete.ID +=1
        super().__init__(attrs)
        self.options = options
        self.value = value
        self.id = "multiauto-"+str(self.id)
    def get_context(self, name, value, attrs):
        value = self.value
        context = super(MultiAutoComplete, self).get_context(name, value, attrs)
        context['options'] = [{'key':('$'+str(i)) if x.pk is None else str(x.pk), 'value':str(x)} for i,x in enumerate(self.options)]
        context['id'] = self.id
        return context
"""
from multiauto.widgets import MultiAutoComplete
m = MultiAutoComplete(options=['lala','jaja','tata'])
m.render(name='teste', value='')

"""

# {{ form.media }}