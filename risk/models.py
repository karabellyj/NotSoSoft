from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def delete(self):
        self.update(is_active=False)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)


class ActiveModel(models.Model):
    is_active = models.BooleanField(default=True, editable=False)

    objects = ActiveManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_active = False
        self.save()


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.BinaryField()
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Risk(models.Model):

    class State(models.TextChoices):
        ACTIVE = 'Active', _('Aktivne')
        CLOSED = 'Closed', _('Uzatovrene')
        HAPPENED = 'Happened', _('Prihodilo sa')

    class Impact(models.TextChoices):
        VVD = 'VVD', _('Velmi velký dopad na projekt')
        VD = 'VD', _('Velký dopad na projekt')
        SD = 'SD', _('Střední dopad na projekt')
        MD = 'MD', _('Malý dopad na projekt')
        VMD = 'VMD', _('Velmi malý dopad na projekt')

    class Probability(models.TextChoices):
        VVP = 'VVP', _('Velmi vysoká pravděpodobnost')
        VP = 'VP', _('Vysoká pravděpodobnost')
        SP = 'SP', _('Střední pravděpodobnost')
        NP = 'NP', _('Nízká pravděpodobnost')
        VNP = 'VNP', _('Velmi nízká pravděpodobnost')

    risk_assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_phase = models.ForeignKey('ProjectPhase', on_delete=models.CASCADE)
    risk_type = models.ForeignKey('RiskType', on_delete=models.CASCADE)
    impact = models.CharField(max_length=3, choices=Impact.choices, default=Impact.VMD)
    state = models.CharField(max_length=20, choices=State.choices, default=State.HAPPENED)
    probability = models.CharField(max_length=3, choices=Probability.choices, default=Probability.VNP)

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    threat = models.TextField()
    starter = models.TextField()
    reactions = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    state_change_date = models.DateField(null=True, blank=True)
    reaction_date = models.DateField(null=True, blank=True)


class Project(ActiveModel):
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    real_end = models.DateField(null=True, blank=True)
    estimated_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class RiskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RiskSubtype(models.Model):
    risk_type = models.ForeignKey('RiskType', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class ProjectPhase(ActiveModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    real_end_date = models.DateField(null=True, blank=True)
    estimated_end_date = models.DateField(null=True, blank=True)

    phase_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'name'], name='unique_projectphase')
        ]

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.pk})
