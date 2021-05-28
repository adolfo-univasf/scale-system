from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

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
    def get_leader_string(self):
        users = self.leader.get_queryset()
        ret = ""
        for us in users:
            ret += us.get_full_name() + ", "
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

