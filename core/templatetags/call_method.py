from django import template
from ministries.utils import my_engaged,my_ministries

register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj,method_name)
    return method(*args)

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_ministry')
def has_ministry(user):
    if my_engaged(user) or my_ministries(user):
        return True
    return False
    
@register.filter(name='has_nconf')
def has_nconf(program_time,user):
    return not program_time.conf(user)
    #return user.groups.filter(name=group_name).exists()

# {% call_method obj 'method_name' args %}
# {% user|filtername : 'arg'%}