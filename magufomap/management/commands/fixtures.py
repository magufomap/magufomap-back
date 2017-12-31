from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create initial fixtures'

    def _create_editors_group(self):
        editors_permissions = [
            'add_poim',
            'change_poim',
            'delete_poim',
            'add_poimimage',
            'change_poimimage',
            'delete_poimimage',
            'change_rating',
            'change_comment',
            'change_changerequest',
        ]

        group, created = Group.objects.get_or_create(name="Editors")
        group.permissions.add(*list(Permission.objects.filter(codename__in=editors_permissions)))
        group.save()

    def handle(self, *args, **options):
        self._create_editors_group()

        self.stdout.write(self.style.SUCCESS('Fixtures created'))
