from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from accounts.models import User
from django.db.models import Q

class MinistryManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(models.Q(name__icontains=query)) #  | models.Q(description__icontains=query)

class Ministry (models.Model):
    name = models.CharField(_("Name"), max_length=50)
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

def fill_database():
    names = ["Sonoplastia", "Diaconato", "Tesouraria", "Recepção", "Ancionato", "Música", "Comunicação", "Escola Sabatina", "Infantil"]
    slug = ["sonoplastia", "diaconato", "tesouraria", "recepcao", "ancionato", "musica", "comunicacao", "escola-sabatina", "infantil"]
    leader = [["jonatas"], ["tiago"], ["kleber"], ["felizarda"], ["jocelio", "kleber", "elias", "jonatas", "tiago"], ["lilian", "jonatas"], ["ana", "tiago"], ["jocelio"], ['ana']]
    functions = [
        [{'name':"Sonoplasta", 'people':["jonatas", "tiago"]},],
        [{'name':"Diacono/Diaconiza", 'people':["jonatas", "tiago"]},],
        [{'name':"Tesoureiro", 'people':["kleber", "tiago", "felizarda"]},],
        [{'name':"Recepcionista", 'people':["felizarda"]},],
        [{'name':"Diretor do Culto", 'people':["jocelio", "kleber", "elias", "jonatas", "tiago"]},
            {'name':"Mensageiro", 'people':["jocelio", "kleber", "elias", "jonatas", "tiago", "nonato"]},],
        [{'name':"Louvor Congregacional", 'people':["jocelio", "elias", "jonatas", "tiago", 'lilian']},
            {'name':"Musica Especial", 'people':["elias", "jonatas", "nonato", "joany", "lilian"]},],
        [{'name':"Apresentador", 'people':["aline", "ana", "jocelio", "kleber", "elias", "jonatas", "tiago"]},],
        [{'name':"Licao da E.S.", 'people':["jocelio", "kleber", "elias", "jonatas", "tiago"]},],
        [{'name':"Adoração Infantil", 'people':["jonatas", "tiago", "ana", "aline"]},],
    ]
    for n,s,le, fun in zip(names, slug, leader, functions):
        mn = Ministry()
        mn.name = n
        mn.slug = s
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