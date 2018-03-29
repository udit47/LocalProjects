from django.http import HttpResponse
from django.template import loader
from .models import Album


def index(request):
    all_albums = Album.objects.all()
    template = loader.get_template('music/index.html')
    return HttpResponse(html)

def detail(request, album_id):
    return HttpResponse("<h2>Details for album_id : " + str(album_id) + "</h2>" )
