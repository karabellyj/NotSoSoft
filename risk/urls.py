from django.urls import path

from .views import (MatrixView, ProjectCreateView, ProjectDeleteView,
                    ProjectDetailView, ProjectListView, ProjectPhaseCreateView,
                    ProjectPhaseDeleteView, ProjectPhaseDetailView,
                    ProjectPhaseUpdateView, ProjectUpdateView, RiskCreateView,
                    RiskDeleteView, RiskDetailView, RiskListView,
                    RiskUpdateView)

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),

    path('project/<int:project_id>/phase/create/', ProjectPhaseCreateView.as_view(), name='project-phase-create'),
    path('project/<int:project_id>/phase/<int:pk>/update/', ProjectPhaseUpdateView.as_view(), name='project-phase-update'),
    path('project/<int:project_id>/phase/<int:pk>/', ProjectPhaseDetailView.as_view(), name='project-phase-detail'),
    path('project/<int:project_id>/phase/<int:pk>/delete/', ProjectPhaseDeleteView.as_view(), name='project-phase-delete'),

    path('project/<int:project_id>/phase/<int:phase_id>/risk/create/', RiskCreateView.as_view(), name='risk-create'),
    path('project/<int:project_id>/phase/<int:phase_id>/risk/<int:pk>/update/', RiskUpdateView.as_view(), name='risk-update'),
    path('project/<int:project_id>/phase/<int:phase_id>/risk/<int:pk>/', RiskDetailView.as_view(), name='risk-detail'),
    path('project/<int:project_id>/phase/<int:phase_id>/risk/<int:pk>/delete/', RiskDeleteView.as_view(), name='risk-delete'),

    path('project/<int:project_id>/register/', RiskListView.as_view(), name='risk-register'),

    path('project/<int:project_id>/matrix/', MatrixView.as_view(), name='matrix')
]
