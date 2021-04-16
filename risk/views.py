from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from users.utils import is_company_manager, is_customer, is_project_manager

from .forms import (CreateProjectForm, CreateProjectPhaseForm, CreateRiskForm,
                    UpdateProjectForm, UpdateProjectPhaseForm, UpdateRiskForm)
from .models import Project, ProjectPhase, Risk


class HomeView(TemplateView):
    template_name = 'home.html'


class ProjectCreateView(PermissionRequiredMixin, BSModalCreateView):
    form_class = CreateProjectForm
    template_name = "risk/project_change.html"
    success_message = 'Success: Project was created.'
    permission_required = ('risk.add_project',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['project_manager'] = self.request.user.pk
        initial['company'] = self.request.user.company.pk
        return initial


class ProjectUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    model = Project
    form_class = UpdateProjectForm
    template_name = "risk/project_change.html"
    permission_required = ('risk.change_project',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProjectListView(ListView):
    model = Project
    template_name = "risk/project_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if is_company_manager(user):
            return qs.filter(company=user.company)
        elif is_project_manager(user):
            return qs.filter(project_manager=user)
        elif is_customer(user):
            return qs.filter(customers__in=[user.pk])
        return qs


class ProjectDetailView(PermissionRequiredMixin, DetailView):
    model = Project
    template_name = "risk/project_detail.html"
    permission_required = ('risk.view_project')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phases'] = ProjectPhase.objects.filter(project=context['object'])

        project_manager = get_user_model().objects.filter(pk=self.object.project_manager.pk)
        phase_managers = get_user_model().objects.filter(pk__in=self.object.projectphase_set.values_list('phase_manager', flat=True).distinct())
        context['users'] = context['object'].customers.all() | project_manager | phase_managers
        return context


class ProjectPhaseCreateView(PermissionRequiredMixin, CreateView):
    form_class = CreateProjectPhaseForm
    template_name = "risk/project_phase_form.html"
    permission_required = ('risk.add_projectphase',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context


class ProjectPhaseUpdateView(PermissionRequiredMixin, UpdateView):
    model = ProjectPhase
    form_class = UpdateProjectPhaseForm
    template_name = "risk/project_phase_change.html"
    permission_required = ('risk.change_projectphase',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context


class ProjectPhaseDetailView(PermissionRequiredMixin, DetailView):
    model = ProjectPhase
    template_name = "risk/project_phase_detail.html"
    permission_required = ('risk.view_projectphase',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["risks"] = Risk.objects.filter(project_phase=context['object'])
        context['project_id'] = self.kwargs['project_id']
        return context


class RiskCreateView(PermissionRequiredMixin, CreateView):
    form_class = CreateRiskForm
    template_name = 'risk/risk_form.html'
    permission_required = ('risk.add_risk',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['project_phase'] = ProjectPhase.objects.get(pk=self.kwargs['phase_id'])
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        context['phase_id'] = self.kwargs['phase_id']
        return context


class RiskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Risk
    form_class = UpdateRiskForm
    template_name = "risk/risk-change.html"
    permission_required = ('risk.change_risk',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        context['phase_id'] = self.kwargs['phase_id']
        return context


class RiskDetailView(PermissionRequiredMixin, DetailView):
    model = Risk
    template_name = "risk/risk_detail.html"
    permission_required = ('risk.view_risk',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        context['phase_id'] = self.kwargs['phase_id']
        return context


class RiskListView(PermissionRequiredMixin, ListView):
    model = Risk
    template_name = "risk/risk-register.html"
    permission_required = ('risk.view_risk',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context
