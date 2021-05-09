from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create regular user"

    def add_arguments(self, parser):
        parser.add_argument("email", help="The user's e-mail address")
        parser.add_argument("password", help="The user's password")
        parser.add_argument("group", help="The user's group")

    def handle(self, **options):
        user_data = {
                "email": options.get("email"),
                "password": options.get("password"),
                }

        TerraUser = get_user_model()

        if not TerraUser.objects.filter(email=user_data['email']).exists():
            user = TerraUser.objects.create_user(**user_data)

            groups = {}
            user_group = options.get("group")
            if user_group:
                if not groups.get(user_group):
                    groups[user_group], _ = Group.objects.get_or_create(name=user_group)
                user.groups.add(groups[user_group])


