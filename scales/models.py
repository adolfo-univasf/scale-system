from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from accounts.models import User

# Create your models here.

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
        return reverse('scales:ministry', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ministry")
        verbose_name_plural = _("Ministries")
        ordering = ['name']
    
class Function (models.Model):
    name = models.CharField(_("Name"), max_length=50)
    ministry = models.ForeignKey("scales.Ministry", verbose_name=_("Ministry"), on_delete=models.CASCADE)
    people = models.ManyToManyField("accounts.User",blank=True, verbose_name=_("People"))
    overload = models.ManyToManyField("scales.Function", blank=True,  verbose_name=_("Overload"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")
        ordering = ['name']

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
        ordering = ['-date']

class ProgramTime(models.Model):
    program = models.ForeignKey("scales.Program", verbose_name=_("Program"), on_delete=models.CASCADE)
    function = models.ForeignKey("scales.Function", verbose_name=_("Function"), on_delete=models.CASCADE)
    time = models.TimeField(_("Time"), auto_now=False, auto_now_add=False, null=True,blank=True)
    person = models.ManyToManyField("accounts.User", verbose_name=_("Person"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    def __str__(self):
        return str(self.program) +" "+ str(self.function)
    class Meta:
        verbose_name = _("Program Time")
        verbose_name_plural = _("Program Times")
        ordering = ['time']