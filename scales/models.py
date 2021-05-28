from django.db import models
from django.utils.translation import gettext as _
from accounts.models import User
from ministries.models import Ministry, Function


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
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def typeprogram(self):
        for l in Program.PROGRAMTYPES:
            if l[0] == self.name:
                return _(l[1])
        return ""
    def __str__(self):
        return self.typeprogram() + ((' '+str(self.date)) if self.date else (" " + _("Template")))

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ['date']

class ProgramTime(models.Model):
    desc = models.CharField(_("Description"), max_length=50, null=True,blank=True)
    program = models.ForeignKey("scales.Program", verbose_name=_("Program"), on_delete=models.CASCADE)
    function = models.ForeignKey("ministries.Function", verbose_name=_("Function"), null=True,blank=True, on_delete=models.SET_NULL)
    lookup = models.ForeignKey("scales.ProgramTime", verbose_name=_("Same as"), on_delete=models.SET_NULL,null=True,blank=True)

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