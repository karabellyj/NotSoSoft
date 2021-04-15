from django.urls import path

from .views import (ProjectCreateView, ProjectDetailView, ProjectListView,
                    ProjectPhaseCreateView, ProjectPhaseDetailView,
                    ProjectPhaseUpdateView, ProjectUpdateView, RiskCreateView,
                    RiskDetailView, RiskUpdateView)

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    path('project/<int:project_id>/create/', ProjectPhaseCreateView.as_view(), name='project-phase-create'),
    path('project/phase/<int:pk>/update/', ProjectPhaseUpdateView.as_view(), name='project-phase-update'),
    path('project/phase/<int:pk>/', ProjectPhaseDetailView.as_view(), name='project-phase-detail'),

    path('project/phase/<int:phase_id>/create/', RiskCreateView.as_view(), name='risk-create'),
    path('project/phase/risk/<int:pk>/update', RiskUpdateView.as_view(), name='risk-update'),
    path('project/phase/<int:pk>/', RiskDetailView.as_view(), name='risk-detail')
]
