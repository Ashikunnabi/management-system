from django.conf import settings


sidebar = {
  'level_0': [
    {
      'details': {
        'title': 'Dashboard',
        'icon': '<i class="feather icon-home"></i>'
      },
      'level_1': [
        {
          'details': {
            'title': 'Default',
            'icon': ''
          },      
        },
        {
          'details': {
            'title': 'Ecommerce',
            'icon': '<i class="feather icon-home"></i>'
          }      
        }
      ]
    },
  ]
}







def template_variables(request):
    variables = {
      'APPLICATION_NAME': settings.APPLICATION_NAME,
      'COMPANY_NAME': 'ALIO',
      'COMPANY_LOGO': '<i class="feather icon-trending-up"></i>'
    }
    return variables