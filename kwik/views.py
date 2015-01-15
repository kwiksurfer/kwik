from django.http import HttpResponse
import datetime


def current_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def tester(request):
    html = "<html><body>Hello</body></html>"
    return HttpResponse(html)
