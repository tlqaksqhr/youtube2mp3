from django.urls import path

from . import views

urlpatterns = [
    path('convert/',views.convert,name='convert'),
    path('available_link/',views.available_link,name='available_link'),
    path('download_link/<video_id>',views.download_link,name='download_link'),
    path('download/<video_id>',views.download,name='download')
]