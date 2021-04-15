from django.conf import settings
from django.db import models
from django.shortcuts import reverse


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.BinaryField()
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Risk(models.Model):
    risk_assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_phase = models.ForeignKey('ProjectPhase', on_delete=models.CASCADE)
    risk_type = models.ForeignKey('RiskType', on_delete=models.CASCADE)
    risk_impacts = models.ForeignKey('RiskImpact', on_delete=models.CASCADE)
    risk_state = models.ForeignKey('RiskState', on_delete=models.CASCADE)
    risk_probability = models.ForeignKey('RiskProbability', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    threat = models.TextField()
    starter = models.TextField()
    reactions = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    state_change_date = models.DateField(null=True, blank=True)
    reaction_date = models.DateField(null=True, blank=True)


class Project(models.Model):
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    real_end = models.DateField(null=True, blank=True)
    estimated_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class RiskProbability(models.Model):
    name = models.CharField(max_length=60)


class RiskType(models.Model):
    name = models.CharField(max_length=255)


class RiskSubtype(models.Model):
    risk_type = models.ForeignKey('RiskType', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class RiskState(models.Model):
    name = models.CharField(max_length=60)


class RiskImpact(models.Model):
    impacts = models.CharField(max_length=60)


class ProjectPhase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    real_end_date = models.DateField(null=True, blank=True)
    estimated_end_date = models.DateField(null=True, blank=True)

    phase_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.pk})
