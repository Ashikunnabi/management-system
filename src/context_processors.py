from django.conf import settings


def template_variables(request):
    variables = {
      'APPLICATION_NAME': settings.APPLICATION_NAME,
      'COMPANY_NAME': 'ALIO',
      'COMPANY_LOGO': '<i class="feather icon-trending-up"></i>'
    }
    return variables