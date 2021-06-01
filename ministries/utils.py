from accounts.models import User
from .models import Ministry, Function
from scales.models import ProgramTime
from functools import reduce

def my_engaged(user):
    def m(x):
        return [x.ministry]
    def r(x,a):
        if x[0] and x[0] not in a:
            a.append(x[0])
        return a
    functions = list(Function.objects.filter(people = user))

    #funções que eu não estou na equipe mas fui colocado na escala
    prog = ProgramTime.objects.filter(person = user)
    for pg in prog:
        functions.append(pg.function)

    if functions:
        return reduce(r,map(m,functions))
    else:
        return []
def my_ministries(user):
     return Ministry.objects.filter(leader=user)