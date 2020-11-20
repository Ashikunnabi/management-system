from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Set all default models objects to setup dafualt db.'

    def handle(self, *args, **options):
        print('[+] Feature: ', end='')
        call_command('loaddata', 'import_sql/feature.json')
        print('[+] Permission: ', end='')
        call_command('loaddata', 'import_sql/permission.json')
        print('[+] Role: ', end='')
        call_command('loaddata', 'import_sql/role.json')
        print('[+] Tenant: ', end='')
        call_command('loaddata', 'import_sql/tenant.json')
        print('[+] User: ', end='')
        call_command('loaddata', 'import_sql/user.json')

