from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from accounts.models import User
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from slugify import slugify

class MinistryManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(models.Q(name__icontains=query)) #  | models.Q(description__icontains=query)

class Ministry (models.Model):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"))
    code = models.SlugField(_("Code"), blank=True) # sistema da tesouraria
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    leader = models.ManyToManyField("accounts.User",blank=True, verbose_name=_("Leadership"))
    objects = MinistryManager()

    def get_absolute_url(self):
        return reverse('ministries:ministry', args=[self.slug])

    def __str__(self):
        return self.name
    def get_leader(self):
        return self.leader.get_queryset()

    def is_leader(self, user):
        return self.leader.get_queryset().filter(pk=user.pk).first()
    def get_leader_string(self):
        users = self.get_leader()
        ret = ""
        for us in users:
            ret += us.get_full_name() + ", "
        return ret
    def get_team(self):
        funcs = Function.objects.filter(ministry = self)
        users = []
        for fn in funcs:
            users +=list(fn.people.get_queryset())

        team = []
        for us in users:
            if us not in team:
                team.append(us)
        team.sort(key=lambda x:x.name)
        return team
    def get_team_string(self):
        team = self.get_team()
        ret = ""
        for t in team:
            ret += str(t) + ", "
        return ret

    def get_functions(self, user):
        return Function.objects.filter(ministry = self, people = user)
    def get_not_functions(self, user):
        fn = list(Function.objects.filter(ministry = self, people = user))
        all = Function.objects.filter(ministry = self)
        return list(filter(lambda x: x not in fn,all))
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)

        ret = super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        leaders = list(self.leader.get_queryset())

        # adicionar usuarios aos grupos automaticamente
        leader_group = Group.objects.get(name='Leader')
        elder_group = Group.objects.get(name='Elder')

        for user in leaders:
            leader_group.user_set.add(user)

        if self.name == 'Ancionato':
            for user in leaders:
                elder_group.user_set.add(user)

        return ret
            
    class Meta:
        verbose_name = _("Ministry")
        verbose_name_plural = _("Ministries")
        ordering = ['name']
    
class Function (models.Model):
    name = models.CharField(_("Name"), max_length=50)
    ministry = models.ForeignKey("ministries.Ministry", verbose_name=_("Ministry"), on_delete=models.CASCADE)
    people = models.ManyToManyField("accounts.User",blank=True, verbose_name=_("People"))
    overload = models.ManyToManyField("ministries.Function", blank=True,  verbose_name=_("Overload"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")
        ordering = ['name']

    def get_people(self):
        return self.people.get_queryset()
    def get_people_string(self):
        users = self.get_people()
        ret = ""
        for us in users:
            ret += us.get_full_name() + ", "
        return ret
    def get_overload(self):
        return self.overload.get_queryset()
    def get_overload_string(self):
        fns = self.get_overload()
        ret = ""
        for fn in fns:
            ret += str(fn) + ", "
        return ret

def fill_database():
    names = ["Sonoplastia", "Diaconato", "Tesouraria", "Recepção", "Ancionato", "Música", "Comunicação", "Escola Sabatina", "Infantil"]
    leader = [["jonatas"], ["tiago"], ["kleber"], ["felizarda"], ["jocelio", "kleber", "elias", "jonatas", "tiago"], ["lilian", "jonatas"], ["ana", "tiago"], ["jocelio"], ['ana']]
    functions = [
        [{'name':"Sonoplasta", 'people':["jonatas", "tiago"], 'overload':
            []},],#(0,0)
        [{'name':"Diacono/Diaconiza", 'people':["jonatas", "tiago"], 'overload':
            []},],#(1,0)
        [{'name':"Tesoureiro", 'people':["kleber", "tiago", "felizarda"], 'overload':
            [(0,0)]},],#(2,0)
        [{'name':"Recepcionista", 'people':["felizarda"], 'overload':
            [(2,0)]},],#(3,0)
        [{'name':"Diretor do Culto", 'people':["jocelio", "kleber", "elias", "jonatas", "tiago"], 'overload':
            [(0,0), (2,0)]},###(4,0)
            {'name':"Mensageiro", 'people':["jocelio", "kleber", "elias", "jonatas", "tiago", "nonato"], 'overload':
            [(4,0), ]},],#(4,1)
        [{'name':"Louvor Congregacional", 'people':["jocelio", "elias", "jonatas", "tiago", 'lilian'], 'overload':
            [(4,1), (4,0), (2,0)]},###(5,0)
            {'name':"Musica Especial", 'people':["elias", "jonatas", "nonato", "joany", "lilian"], 'overload':
            [(5,0), (4,1), (4,0), (3,0), (2,0), (1,0)]},],#(5,1)
        [{'name':"Apresentador", 'people':["aline", "ana", "jocelio", "kleber", "elias", "jonatas", "tiago"], 'overload':
            [(5,1), (5,0), (4,1), (4,0), (2,0), (0,0)]},],#(6,0)
        [{'name':"E.S. Adultos", 'people':["jocelio", "kleber", "elias", "jonatas", "tiago"], 'overload':
            [(6,0), (5,1), (5,0), (4,1), (4,0), (2,0), (1,0), (0,0)]},#(7,0)
            {'name':"E.S. Adolescentes", 'people':["aline"], 'overload':
            [(1,0),(2,0), (4,1), (5,1), (6,0)]},#(7,1)
            {'name':"E.S. Primários", 'people':["edcleuma"], 'overload':
            [(1,0),(2,0), (4,1), (5,1), (6,0)]},#(7,2)
            {'name':"E.S. Juvenis", 'people':["ana"], 'overload':
            [(1,0),(2,0), (4,1), (5,1), (6,0)]},],#(7,3)
        [{'name':"Adoração Infantil", 'people':["jonatas", "tiago", "ana", "aline"], 'overload':
            [(7,3),(7,2),(7,1), (7,0), (6,0), (5,1), (5,0), (4,1), (4,0), (3,0), (0,0)]},],#(8,0)
    ]
    for n,le,fun in zip(names, leader, functions):
        mn = Ministry()
        mn.name = n
        mn.save()
        for l in le:
            mn.leader.add(User.objects.filter(username=l).first())
        for f in fun:
            fn = Function()
            fn.name = f['name']
            fn.ministry = mn
            fn.save()
            for p in f['people']:
                fn.people.add(User.objects.filter(username=p).first())
            f['ob'] = fn
        mn.save()
    for fun in functions:
        for f in fun:
            for ov in f['overload']:
                f['ob'].overload.add(functions[ov[0]][ov[1]]['ob'])
                functions[ov[0]][ov[1]]['ob'].overload.add(f['ob'])
    
    leader_group = Group.objects.get(name='Leader')
    elder_group = Group.objects.get(name='Elder')

    crud_function = list(Permission.objects.filter(name__icontains = 'function'))
    crud_ministry = Permission.objects.filter(name__icontains = 'function')

    for perm in crud_function + [crud_ministry.filter(name__icontains = 'change').first()]:
        leader_group.permissions.add(perm)
    crud_ministry = list(crud_ministry)

    for perm in crud_function + crud_ministry:
        elder_group.permissions.add(perm)
    
# from accounts.models import User
# from ministries.models import Ministry, Function