from django.contrib.auth import get_user_model
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from users.utils import is_company_manager, is_project_manager

from .forms import (CreateProjectForm, CreateProjectPhaseForm, CreateRiskForm,
                    UpdateProjectForm, UpdateProjectPhaseForm, UpdateRiskForm)
from .models import Project, ProjectPhase, Risk


class HomeView(TemplateView):
    template_name = 'home.html'


class ProjectCreateView(CreateView):
    form_class = CreateProjectForm
    template_name = "risk/project_change.html"

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


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = UpdateProjectForm
    template_name = "risk/project_change.html"

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
        return qs


class ProjectDetailView(DetailView):
    model = Project
    template_name = "risk/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phases'] = ProjectPhase.objects.filter(project=context['object'])

        project_manager = get_user_model().objects.filter(pk=self.object.project_manager.pk)
        phase_managers = get_user_model().objects.filter(pk__in=self.object.projectphase_set.values_list('phase_manager', flat=True).distinct())
        context['users'] = context['object'].customers.all() | project_manager | phase_managers
        return context


class ProjectPhaseCreateView(CreateView):
    form_class = CreateProjectPhaseForm
    template_name = "risk/project_phase_form.html"

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


class ProjectPhaseUpdateView(UpdateView):
    model = ProjectPhase
    form_class = UpdateProjectPhaseForm
    template_name = "risk/project_phase_change.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context


class ProjectPhaseDetailView(DetailView):
    model = ProjectPhase
    template_name = "risk/project_phase_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["risks"] = Risk.objects.filter(project_phase=context['object'])
        context['project_id'] = self.kwargs['project_id']
        return context


class RiskCreateView(CreateView):
    form_class = CreateRiskForm
    template_name = 'risk/risk_form.html'

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


class RiskUpdateView(UpdateView):
    model = Risk
    form_class = UpdateRiskForm
    template_name = "risk/risk-change.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        context['phase_id'] = self.kwargs['phase_id']
        return context


class RiskDetailView(DetailView):
    model = Risk
    template_name = "risk/risk-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        context['phase_id'] = self.kwargs['phase_id']
        return context


class RiskListView(ListView):
    model = Risk
    template_name = "risk/risk-register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context
