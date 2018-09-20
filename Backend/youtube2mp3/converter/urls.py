from django.urls import path

from . import views

urlpatterns = [
    path('convert/',views.convert,name='convert'),
    path('download/',views.download,name='download')
]