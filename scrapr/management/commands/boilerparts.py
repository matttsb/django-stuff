from django.core.management.base import BaseCommand, CommandError
from heating.models import *
from bs4 import *
import os

#todo: manufacturers could be added from this

# python manage.py boilerparts
class Command(BaseCommand):
    help = 'Inserts all boiler data from boilerparts site'

    def handle(self, *args, **options):
        directory = os.fsencode("/home/mattburke/boilerdata/")

        for entry in os.scandir(directory):
            with open(entry.path, "r") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                desc = [x.find('button')['data-desc'] for x in soup.find_all('div', class_= "product-item")]
                mpn = [x.find('button')['data-mpn'] for x in soup.find_all('div', class_= "product-item")]
                price = [x.find('button')['data-price'] for x in soup.find_all('div', class_= "product-item")]
                man = [x.find('button')['data-man'] for x in soup.find_all('div', class_= "product-item")]
                for i in range(0, len(mpn)):
                    notes=""
                    if "for" in desc[i]:
                        desc[i]=desc[i].split('for')[0]
                    if " - " in desc[i]:
                        notes=desc[i].split('-')[-1]
                        desc[i]=desc[i].split('-')[0]
                    #try:
                        #Parttypes.objects.create_part(desc[i].strip())
                    #except:
                        #self.stdout.write(self.style.NOTICE(desc[i].strip()))
            
                    try:
                        man , created = Manufacturer.objects.get_or_create(name=man[i],website='http://')
                    except:
                        print ("bad manu")
                    try:
                        part, created=  Part.objects.get_or_create(mpn=mpn[i],price=price[i],man_id=1,parttype=Parttypes.objects.get(name=desc[i].strip()))
                        part.price= price[i]
                        part.dim=notes
                        part.man=man
                        part.parttype =Parttypes.objects.get(name=desc[i].strip())
                        part.save()
                    except:
                        print(desc[i].strip(),mpn)