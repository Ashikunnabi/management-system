from django.conf import settings


def template_variables(request):
    variables = {
      'APPLICATION_NAME': settings.APPLICATION_NAME,
      'COMPANY_NAME': settings.COMPANY_NAME,
      'FAVICON_URL': settings.FAVICON_URL,
      'COMPANY_NAME_ICON_URL': settings.COMPANY_NAME_ICON_URL
    }
    return variables