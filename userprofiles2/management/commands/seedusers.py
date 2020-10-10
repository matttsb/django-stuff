from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from userprofiles2.models import UserProfile
import os
import csv

#password:   PJ3MGGjg6z3g8M@
#USAGE: ./manage.py seedusers 200usernames.txt 
class Command(BaseCommand):
    help = 'Seeds user table'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Indicates filename containing users to be created')


    def handle(self, *args, **kwargs):
        print ("Importing " + kwargs['file'])
        with open(kwargs['file'], 'rt') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', )
            for line in lines:
                username=line[0].strip()
                print ("Creating " + username)
                user , created = User.objects.get_or_create(username = username)
                user.save()
                userProfile, created=UserProfile.objects.get_or_create(user = user)
                userProfile.save()
                
               