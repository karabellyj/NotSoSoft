import tempfile
from collections import Counter

from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalDeleteView,
                                           BSModalUpdateView)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import Group
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from weasyprint import CSS, HTML

from users.utils import is_company_manager, is_customer, is_project_manager

from .forms import (CreateProjectForm, CreateProjectPhaseForm, CreateRiskForm,
                    UpdateProjectForm, UpdateProjectPhaseForm, UpdateRiskForm)
from .models import Project, ProjectPhase, Risk, RiskType


class ProjectCreateView(PermissionRequiredMixin, BSModalCreateView):
    form_class = CreateProjectForm
    template_name = "risk/project_form.html"
    success_message = 'Success: Project was created.'
    permission_required = ('risk.add_project',)
    success_url = reverse_lazy('project-list')

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


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "risk/project_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        q = self.request.GET.get('q')
        active = self.request.GET.get('active', 'true')

        if is_company_manager(user):
            qs = qs.filter(company=user.company)
        elif is_project_manager(user):
            qs = qs.filter(project_manager=user)
        elif is_customer(user):
            qs = qs.filter(customers__in=[user.pk])

        if q:
            qs = qs.filter(name__istartswith=q)
        if active == 'true':
            qs = qs.active()
        if active == 'false':
            qs = qs.inactive()

        return qs


class ProjectDetailView(PermissionRequiredMixin, DetailView):
    model = Project
    template_name = "risk/project_detail.html"
    permission_required = ('risk.view_project')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.object.pk
        active = self.request.GET.get('active', 'true')
        q = self.request.GET.get('q')
        role = self.request.GET.get('role')
        context['roles'] = Group.objects.all()

        context['phases'] = ProjectPhase.objects.filter(project=context['object'])
        if active == 'true':
            context['phases'] = context['phases'].active()
        elif active == 'false':
            context['phases'] = context['phases'].inactive()

        project_manager = get_user_model().objects.filter(pk=self.object.project_manager.pk)
        phase_managers = get_user_model().objects.filter(pk__in=self.object.projectphase_set.values_list('phase_manager', flat=True).distinct())
        context['users'] = context['object'].customers.all() | project_manager | phase_managers
        if q:
            context['users'] = context['users'].annotate(fullname=Concat(
                'first_name', Value(' '), 'last_name')).filter(Q(fullname__istartswith=q) | Q(fullname__icontains=q) | Q(username__istartswith=q))
        if role:
            context['users'] = context['users'].filter(groups__name=role)

        return context


class ProjectDeleteView(BSModalDeleteView):
    model = Project
    template_name = "risk/project_confirm_delete.html"
    success_url = reverse_lazy('project-list')
    success_message = "OK"


class ProjectPhaseCreateView(PermissionRequiredMixin, BSModalCreateView):
    form_class = CreateProjectPhaseForm
    template_name = "risk/project_phase_form.html"
    permission_required = ('risk.add_projectphase',)

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.kwargs['project_id']})

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


class ProjectPhaseUpdateView(PermissionRequiredMixin, BSModalUpdateView):
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
        state = self.request.GET.get('state')

        context["risks"] = Risk.objects.filter(project_phase=context['object'])
        if state:
            context['risks'] = context['risks'].filter(state=state)

        context['project_id'] = self.kwargs['project_id']
        context['states'] = Risk.State.choices
        return context


class ProjectPhaseDeleteView(BSModalDeleteView):
    model = ProjectPhase
    template_name = 'risk/project_phase_confirm_delete.html'
    success_message = "OK"

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.kwargs['project_id']})


class RiskCreateView(PermissionRequiredMixin, BSModalCreateView):
    form_class = CreateRiskForm
    template_name = 'risk/risk_form.html'
    permission_required = ('risk.add_risk',)

    def get_success_url(self):
        return reverse_lazy('project-phase-detail', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['phase_id']})

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


class RiskUpdateView(PermissionRequiredMixin, BSModalUpdateView):
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
        context['phases'] = ProjectPhase.objects.filter(project__pk=self.kwargs['project_id'])
        context['risk_types'] = RiskType.objects.all()

        context['probabilities'] = Risk.Probability.choices
        context['impacts'] = Risk.Impact.choices
        context['states'] = Risk.State.choices
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(project_phase__project=self.kwargs['project_id'])
        q = self.request.GET.get('q')
        phase = self.request.GET.get('phase')
        risk_type = self.request.GET.get('risk_type')
        probas = self.request.GET.getlist('probability')
        impacts = self.request.GET.getlist('impact')
        states = self.request.GET.getlist('state')

        if q:
            qs = qs.filter(name__istartswith=q)

        if phase:
            qs = qs.filter(project_phase__pk=phase)
        if risk_type:
            qs = qs.filter(risk_type__pk=risk_type)

        if probas:
            qs = qs.filter(probability__in=probas)
        if impacts:
            qs = qs.filter(impact__in=impacts)
        if states:
            qs = qs.filter(state__in=states)
        return qs


class RiskDeleteView(BSModalDeleteView):
    model = Risk
    template_name = "risk/risk_confirm_delete.html"
    success_message = "OK"

    def get_success_url(self):
        return reverse_lazy('project-phase-detail', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['phase_id']})


class MatrixView(TemplateView):
    template_name = 'risk/matrix.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']

        risks = Risk.objects.filter(project_phase__project=project_id).all()

        matrix = dict(zip(map(lambda x: x[0], Risk.Probability.choices), [[[] for _ in range(len(Risk.Impact))] for _ in range(len(Risk.Probability))]))
        impacts_to_id = dict(zip(map(lambda x: x[0], Risk.Impact.choices), range(0, len(Risk.Impact))))

        for risk in risks:
            matrix[risk.probability][impacts_to_id[risk.impact]].append(risk)

        context['matrix'] = matrix
        context['impacts'] = impacts_to_id.keys()
        return context


class StatsView(TemplateView):
    template_name = 'risk/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        risks = Risk.objects.filter(project_phase__project__company=self.request.user.company)

        context['num_happened_risks'] = risks.filter(state='Happened').count()
        context['num_active_projects'] = Project.objects.filter(company=self.request.user.company).active().count()
        context['num_vvhr_risks'] = len([risk for risk in risks.all() if risk.risk == 'VVHR'])

        context['risk_states'] = risks.values('state').order_by('state').annotate(count=Count('state'))
        context['risk_values'] = Counter([risk.risk for risk in risks]).items()
        return context


def generate_pdf(request, risk_id):
    risk = Risk.objects.get(pk=risk_id)

    html_string = render_to_string('risk/pdf_template.html', {'object': risk}, request).encode(encoding='utf-8')
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[CSS(settings.BASE_DIR / 'static/css/bootstrap.min.css')])

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = f'inline; filename={risk.name}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


class StatisticsView(TemplateView):
    model = Project
    template_name = "risk/statistics.html"
