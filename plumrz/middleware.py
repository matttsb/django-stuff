from django.http import HttpResponse
import os
from django.conf import settings

from bs4 import BeautifulSoup as BSHTML

class FixStuffMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        file_contents = open(os.path.join(settings.MEDIA_ROOT, 'bad-user-agents.list'), 'r').read()
        self.agents = file_contents.split("\n")
      

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        try:
            contenttype=response['Content-Type']
        except:
            contenttype=""
        
        if contenttype == "text/html; charset=utf-8":
            response_text=str(response.content,encoding='UTF-8')
#            response_text=response_text.replace('and','xxx')
            soup = BSHTML(response_text,features="lxml")
            images = soup.findAll('img')
            title=""
            alt=""
            for image in images:
  
                try:
                    alt = image['alt']
                except:
                    if not alt:
                        alt=image['src'].replace("/media/img/","").replace(".jpg","").replace("_"," ").replace("-"," ") 
                
                try:
                    title = (image['title'])
                except:
                    if not title:
                        image['title']=alt

            response_text=str(soup)
            response.content = bytes(response_text,encoding='UTF-8')
        
        for i in self.agents:
            if i in request.META['HTTP_USER_AGENT']:
                print (request.META['HTTP_USER_AGENT'])
                print (i)
                response.content=bytes("",encoding='UTF-8')
            # Code to be executed for each request/response after
        # the view is called.

        return response
