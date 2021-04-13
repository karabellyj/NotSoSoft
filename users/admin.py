from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from risk.models import Company

from .forms import AdminUserCreationForm
from .models import CustomUser
from .utils import is_company_manager


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'company', 'groups', 'is_staff')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if is_company_manager(request.user):
            if 'company' in form.base_fields:
                form.base_fields['company'].queryset = Company.objects.filter(pk=request.user.company.pk)

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and is_company_manager(request.user):
            return qs.filter(company=request.user.company)
        return qs
