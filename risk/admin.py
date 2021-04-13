from django.contrib import admin

from users.utils import (get_customers_qs, get_project_managers_qs,
                         is_company_manager)

from .models import Company, Project


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and is_company_manager(request.user):
            return qs.filter(pk=request.user.company.pk)
        return qs


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['project_manager'].queryset = get_project_managers_qs(company=request.user.company)
        form.base_fields['customers'].queryset = get_customers_qs(company=request.user.company)

        if not request.user.is_superuser and is_company_manager(request.user):
            form.base_fields['company'].queryset = Company.objects.filter(pk=request.user.company.pk)

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and is_company_manager(request.user):
            return qs.filter(company=request.user.company)
        return qs
