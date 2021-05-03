from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import DateTimeInput, HiddenInput, ValidationError

from users.utils import (get_customers_qs, get_phase_manager_qs,
                         get_project_managers_qs)

from .models import Project, ProjectPhase, Risk


class CreateProjectForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = get_customers_qs(company=user.company)

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'project_manager': HiddenInput,
            'company': HiddenInput,
        }


class UpdateProjectForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = get_customers_qs(company=user.company)

    class Meta:
        model = Project
        fields = ('name', 'description', 'start_date', 'real_end', 'estimated_end_date', 'customers')


class CreateProjectPhaseForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['phase_manager'].queryset = get_phase_manager_qs(company=user.company)

    class Meta:
        model = ProjectPhase
        fields = '__all__'
        widgets = {
            'project': HiddenInput,
            'start_date': DateTimeInput
        }

    def full_clean(self):
        super().full_clean()
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e)


class UpdateProjectPhaseForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['phase_manager'].queryset = get_phase_manager_qs(company=user.company)

    class Meta:
        model = ProjectPhase
        fields = ('name', 'description', 'start_date', 'real_end_date', 'estimated_end_date', 'phase_manager')


class CreateRiskForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['risk_assignee'].queryset = get_project_managers_qs(company=user.company) | get_phase_manager_qs(company=user.company)

    class Meta:
        model = Risk
        fields = '__all__'
        widgets = {
            'project_phase': HiddenInput
        }


class UpdateRiskForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['risk_assignee'].queryset = get_project_managers_qs(company=user.company) | get_phase_manager_qs(company=user.company)

    class Meta:
        model = Risk
        exclude = ('project_phase',)
