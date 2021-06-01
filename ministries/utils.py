from accounts.models import User
from .models import Ministry, Function
from functools import reduce

def my_engaged(user):
    def m(x):
        return [x.ministry]
    def r(x,a):
        if x[0] not in a:
            a.append(x[0])
        return a
    functions = Function.objects.filter(people = user)
    if functions.first():
        return reduce(r,map(m,functions))
    else:
        return []
def my_ministries(user):
     return Ministry.objects.filter(leader=user)