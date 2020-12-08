from django.http import HttpResponse

from bs4 import BeautifulSoup as BSHTML

class FixStuffMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        if response['Content-Type'] == "text/html; charset=utf-8":
            response_text=str(response.content,encoding='UTF-8')
#            response_text=response_text.replace('and','xxx')
            soup = BSHTML(response_text)
            images = soup.findAll('img')
            for image in images:
                if image['alt']=="":
                    image['alt']=image['src'].replace("/media/img/","").replace(".jpg","").replace("_"," ").replace("-"," ")
                try:
                    _title = (image['title'])
                except:
                    image['title']= image['alt']
            response_text=str(soup)
            response.content = bytes(response_text,encoding='UTF-8')
      

        # Code to be executed for each request/response after
        # the view is called.

        return response