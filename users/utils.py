from .models import CustomUser


def is_company_manager(user):
    return user.groups.filter(name='company_manager').exists()


def is_project_manager(user):
    return user.groups.filter(name='project_manager').exists()


def is_customer(user):
    return user.groups.filter(name='customer').exists()


def get_project_managers_qs(company=None):
    qs = CustomUser.objects.filter(groups__name='project_manager')
    if company:
        return qs.filter(company=company)
    return qs


def get_phase_manager_qs(company=None):
    qs = CustomUser.objects.filter(groups__name='phase_manager')
    if company:
        return qs.filter(company=company)
    return qs


def get_customers_qs(company=None):
    qs = CustomUser.objects.filter(groups__name='customer')
    if company:
        return qs.filter(company=company)
    return qs
