from django.http import HttpResponse
import os
import datetime

this_path = os.getcwd()

def current_time(request):
    now = datetime.datetime.now()
    html = "<html><body><p>It is now %s.</p><p>Directory: %s</body></html>" % (now, this_path)
    return HttpResponse(html)

def tester(request):
    html = "<html><body>Hello</body></html>"
    return HttpResponse(html)
