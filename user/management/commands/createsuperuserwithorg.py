"""
This module contains a Django management command to create
a super user with an associated organization.
"""

from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from user.models import Organisation, User


class Command(BaseCommand):
    """
    Custom management command to create a user with an associated organization.

    Usage: python manage.py createuserwithorg --username [USERNAME] --email [EMAIL] --organisation [ORG_PK]

    Args:
        --username (str): Username for the user.
        --email (str): Email for the user.
        --organisation (int): Primary key (PK) of the organization for the user.
    """

    help = 'Create a user with an associated organization'

    def add_arguments(self, parser):
        """
        Add command-line arguments to the management command.
        """
        parser.add_argument('--username', type=str,
                            help='Username for the user')
        parser.add_argument('--email', type=str, help='Email for the user')
        parser.add_argument('--organisation', type=int,
                            help='PK of the organization for the user')

    def handle(self, *args, **options):
        """
        Handle the execution of the management command.
        """
        username = options['username']
        email = options['email']
        organisation_pk = options['organisation']

        try:
            org = Organisation.objects.get(pk=organisation_pk)
        except Organisation.DoesNotExist:
            raise CommandError(
                f"Organization with PK {organisation_pk} does not exist.")

        password = getpass('Enter password: ')
        confirm_password = getpass('Confirm password: ')

        if password != confirm_password:
            raise CommandError('Passwords do not match.')

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                organisation=org,
            )
        except Exception as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS(
            f"Superuser '{username}' with organization '{org}' created successfully."))

