from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('convert', views.convert, name='convert'),
    path('download/<str:name>', views.download, name='download'),
    path('convert/<str:name>/<str:format>/<str:resolution>', views.convert_video, name='convert'),
    path('privacy', views.privacy, name='privacy'),
]
