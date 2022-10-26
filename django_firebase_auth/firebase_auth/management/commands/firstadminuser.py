from django.contrib.auth.models import UserManager
from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand
from firebase_auth.utils import create_super_user


class Command(UserManager, SuperUserCommand):
    def handle(self, *args, **options):
        try:
            create_super_user('admin@example.com', '1mytestuser!', 'admin')
            print("User admin@example.com was created and added to Firebase and local DB successfully")
        except:
            print("User admin@example.com was created already - it is not your first call of this command !")
