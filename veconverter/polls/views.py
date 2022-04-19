import mimetypes
import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from polls.services.YoutubeService import YoutubeService
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    context = {
        'title': "Save your favorite song/video now!",
    }
    return render(request, 'polls/index.html', context)


def convert(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        format = request.POST.get('format')
        converter = YoutubeService(url)

        if format == 'mp3':
            name = converter.convert_to_mp3()
            context = {
                'title': "Yey, your url is converted!",
                'url': url,
                'format': format,
                'name': name,
                'thumbnail': converter.get_thumbnail(),
                'embed': converter.get_embed_url(),
            }
        else:
            context = {
                'title': "Please select a resolution!",
                'url': url,
                'format': format,
                'name': "Name",
                'resolutions': converter.get_resolutions(),
                'thumbnail': converter.get_thumbnail(),
                'embed': converter.get_embed_url(),
            }

        return render(request, 'polls/convert.html', context)

    return render(request, 'polls/index.html', context={'title': "Save your favorite song/video now!", })


def download(request, name):
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/" + name

    path = open(file_path, 'rb')
    mime_types, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(path, content_type=mime_types)
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response


@csrf_exempt
def convert_video(request, name, format, resolution):
    url = "https://www.youtube.com/watch?v=" + name
    converter = YoutubeService(url)
    name = converter.get_resolution_by_id(resolution)
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/" + name

    return JsonResponse({
        'url': url,
        'format': format,
        'name': name,
        'file': file_path,
        'status': 'success',
    })


def privacy(request):
    return render(request, 'polls/privacy.html', context={'title': "Privacy Policy", })
