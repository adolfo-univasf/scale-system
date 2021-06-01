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
        self.options = options
        self.value = value
        attrs['id'] = "multiauto-"+str(self.id)
        super().__init__(attrs)
    def get_context(self, name, value, attrs):
        value = value if value else self.value
        context = super(MultiAutoComplete, self).get_context(name, value, attrs)
        context['options'] = list(map(lambda x:str(x),self.options))
        return context
"""
from scales.widgets import MultiAutoComplete
m = MultiAutoComplete(options=['lala','jaja','tata'])
m.render(name='teste', value='')

"""

# {{ form.media }}