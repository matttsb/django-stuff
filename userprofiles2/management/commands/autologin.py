from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from userprofiles2.models import UserProfile
import os
import csv
from sesame.utils import get_query_string

class Command(BaseCommand):
    help = 'Generate magic login links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', 
            type=str, 
            help='Username to generate link for'
            )

    def handle(self, *args, **kwargs):
        if kwargs['username']:
            user = User.objects.get(username = kwargs['username'])
            print (get_query_string(user))
        else:
            for u in User.objects.all():
                print (u.username)
                print ("http://0.0.0.0:8000" +get_query_string(u))

                
               