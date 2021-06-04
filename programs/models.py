from django.db import models

from django.utils.translation import gettext as _
from accounts.models import User
from ministries.models import Ministry, Function
from datetime import time, datetime, timedelta


# Create your models here.

class Program (models.Model):
    SATURDAY = 'SA'
    SATURDAYAFTERNOON = 'JA'
    WEDNESDAY = 'WE'
    SUNDAY = 'SN'
    FRIDAY = 'FR'
    SPECIAL = 'SP'
    WEEKPFPRAYER = 'WP'

    PROGRAMTYPES = [
        (SATURDAY, _('Saturday')),
        (SATURDAYAFTERNOON, _('Saturday afternoon')),
        (WEDNESDAY, _('Wednesday')),
        (SUNDAY,_('Sunday')),
        (FRIDAY, _('Friday')),
        (SPECIAL, _('Special')),
        (WEEKPFPRAYER,_('Week of Prayer'))
    ]
    name = models.CharField(
        max_length=2,
        choices=PROGRAMTYPES
    )
    description = models.TextField(_('Simple Description'), blank=True)
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False, null=True,blank=True)
    image = models.ImageField(_("Image"), upload_to='program',null=True,blank=True)
    transmission = models.URLField(_("Transmission Link"), max_length=200,null=True,blank=True)
    room = models.URLField(_("Room Link"), max_length=200,null=True,blank=True)
    presential = models.BooleanField(_("Presential?"),default=False)
    iscription = models.BooleanField(_("Needs subscription?"),default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def typeprogram(self):
        for l in Program.PROGRAMTYPES:
            if l[0] == self.name:
                return _(l[1])
        return ""
    def __str__(self):
        return self.typeprogram() + ((' '+str(self.date)) if self.date else (" " + _("Template")))
    
    @property
    def datetime(self):
        t = ProgramTime.objects.filter(program = self, time__isnull=False).first()
        d = self.date
        if t:
            t = t.time
        else:
            t = time(0,0,0)
        return datetime(d.year, d.month, d.day, t.hour, t.minute)
    
    @property
    def enddatetime(self):
        t = ProgramTime.objects.filter(program = self, time__isnull=False).last()
        d = self.date
        if t:
            t = t.time
        else:
            t = datetime.now() + timedelta(0,60)
        return datetime(d.year, d.month, d.day, t.hour, t.minute)

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ['date']

class ProgramTime(models.Model):
    desc = models.CharField(_("Description"), max_length=50, null=True,blank=True)
    program = models.ForeignKey("programs.Program", verbose_name=_("Program"), on_delete=models.CASCADE)
    function = models.ForeignKey("ministries.Function", verbose_name=_("Function"), null=True,blank=True, on_delete=models.SET_NULL)
    lookup = models.ForeignKey("programs.ProgramTime", verbose_name=_("Same as"), on_delete=models.SET_NULL,null=True,blank=True)

    time = models.TimeField(_("Time"), auto_now=False, auto_now_add=False, null=True,blank=True)
    person = models.ManyToManyField("accounts.User", verbose_name=_("Person"), blank=True, related_name="person")
    confirmmed = models.ManyToManyField("accounts.User", verbose_name=_("Confirmmed"), blank=True, related_name="confirmmed")
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    def __str__(self):
        return str(self.program) +" "+ self.name()
    class Meta:
        verbose_name = _("Program Time")
        verbose_name_plural = _("Program Times")
        ordering = ['program__date','program__name','time']

    def people(self):
        return self.person.get_queryset() if len(self.person.get_queryset()) else self.lookup.people() if self.lookup else []

    def name(self):
        return str(self.desc) if self.desc else str(self.function)

    def func(self):
        return self.function if self.function else self.lookup.func()
    def conf(self, user):
        return self.confirmmed.filter(pk = user.pk)

    def n_confirmmed (self):
        ps = list(self.person.get_queryset())
        cn = list(self.confirmmed.get_queryset())
        return list(filter(lambda x: x not in cn, ps))

def fill_database():
    di = [
        {'name':'SA', 'desc': 'Nosso típico culto de sábado de manha, com a apresentação da lição da escola sabatina, momento para as crianças, musicas e uma mensagem especial.', 'programtime':[
            {'desc':'Louvor e Oração', "function":Function.objects.get(name="Louvor Congregacional"), "time":time(9,0), 
                'lookup':None},
            {'desc':'Informativo', "function":None, "time":time(9,5),
                'lookup':None},
            {'desc':'Licao da E.S.', "function":Function.objects.get(name="E.S. Adultos"), "time":time(9,11),
                'lookup':None},
            {'desc':'470 O senhor está aqui', "function":None, "time":time(9,45),
                'lookup':0},
            {'desc':'Avisos', "function":Function.objects.get(name="Apresentador"), "time":time(9,47),
                'lookup':13},
            {'desc':'Provai e Vede', "function":None, "time":time(9,52),
                'lookup':None},
            {'desc':'Quero Ofertar', "function":None, "time":time(9,57),
                'lookup':0},
            {'desc':'Adoração Infantil', "function":Function.objects.get(name="Adoração Infantil"), "time":time(10,2),
                'lookup':None},
            {'desc':'Musica Especial', "function":Function.objects.get(name="Musica Especial"), "time":time(10,7),
                'lookup':None},
            {'desc':'Pregação', "function":Function.objects.get(name="Mensageiro"), "time":time(10,12),
                'lookup':None},
            {'desc':'Musica Especial', "function":None, "time":time(10,42),
                'lookup':8},
            {'desc':'Oração', "function":None, "time":time(10,47),
                'lookup':9},
            {'desc':'Sonoplasta', "function":Function.objects.get(name="Sonoplasta"), "time":None,
                'lookup':None},
            {'desc':'Diretor do Culto', "function":Function.objects.get(name="Diretor do Culto"), "time":None,
                'lookup':None},
            {'desc':'Diácono', "function":Function.objects.get(name="Diacono/Diaconiza"), "time":None,
                'lookup':None},
            {'desc':'Tesoureiro', "function":Function.objects.get(name="Tesoureiro"), "time":None,
                'lookup':None},
            {'desc':'Recepcionista', "function":Function.objects.get(name="Recepcionista"), "time":None,
                'lookup':None},
            {'desc':'E.S. Adolescentes', "function":Function.objects.get(name="E.S. Adolescentes"), "time":None,
                'lookup':None},
            {'desc':'E.S. Juvenis', "function":Function.objects.get(name="E.S. Juvenis"), "time":None,
                'lookup':None},
            {'desc':'E.S. Primários', "function":Function.objects.get(name="E.S. Primários"), "time":None,
                'lookup':None},
        ]},
        {'name':'SN', 'desc': 'Culto de domingo com louvores, momento para as crianças, momento de oração e uma mensagem evangelística com foco nos amigos convidados', 'programtime':[
            {'desc':'Louvor e Oração', "function":Function.objects.get(name="Louvor Congregacional"), "time":time(19,15),
                'lookup':None},
            {'desc':'Boas Vindas', "function":None, "time":time(19,30),
                'lookup':3},
            {'desc':'Adoração Infantil', "function":None, "time":time(19,35),
                'lookup':None},
            {'desc':'Avisos', "function":Function.objects.get(name="Apresentador"), "time":time(19,40),
                'lookup':10},
            {'desc':'Musica Especial', "function":Function.objects.get(name="Musica Especial"), "time":time(19,45),
                'lookup':None},
            {'desc':'Pregação', "function":Function.objects.get(name="Mensageiro"), "time":time(19,50),
                'lookup':None},
            {'desc':'Musica Especial', "function":None, "time":time(20,20),
                'lookup':4},
            {'desc':'Oração', "function":None, "time":time(20,25),
                'lookup':5},
            {'desc':'Encerramento', "function":None, "time":time(20,27),
                'lookup':3},
            {'desc':'Sonoplasta', "function":Function.objects.get(name="Sonoplasta"), "time":None,
                'lookup':None},
            {'desc':'Diretor do Culto', "function":Function.objects.get(name="Diretor do Culto"), "time":None,
                'lookup':None},
        ]},
        {'name':'WE', 'desc': 'Culto de oração, feito ainda no conforto da sua casa, atraves da transmissão pelo zoom. Com louvores, um momento de oração e uma mensagem inspirada no devocional de cada dia.', 'programtime':[
            {'desc':'Boas Vindas', "function":None, "time":time(20,0),
                'lookup':2},
            {'desc':'Louvor', "function":None, "time":time(20,5),
                'lookup':6},
            {'desc':'Momento de Oração', "function":Function.objects.get(name="Apresentador"), "time":time(20,15),
                'lookup':7},
            {'desc':'Pregação', "function":Function.objects.get(name="Mensageiro"), "time":time(20,25),
                'lookup':None},
            {'desc':'Oração', "function":None, "time":time(20,57),
                'lookup':3},
            {'desc':'Encerramento', "function":None, "time":time(20,59),
                'lookup':2},
            {'desc':'Sonoplasta', "function":Function.objects.get(name="Sonoplasta"), "time":None,
                'lookup':None},
            {'desc':'Diretor do Culto', "function":Function.objects.get(name="Diretor do Culto"), "time":None,
                'lookup':None},
        ]},
    ]
    for d in di:
        pr = Program()
        pr.name = d['name']
        pr.description = d['desc']
        pr.save()

        for pgt in d['programtime']:
            pt = ProgramTime()
            pt.program = pr
            pt.desc = pgt['desc']
            pt.time = pgt['time']
            pt.function = pgt['function']
            pt.save()
            pgt['ob'] = pt

        for pgt in d['programtime']:
            if pgt['lookup'] is not None:
                pgt['ob'].lookup = d['programtime'][pgt['lookup']]['ob']
                pgt['ob'].save()
