from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('recognize-faces/', views.recognize_faces, name='recognize_faces'),
    path('video-capture/', views.video_capture, name = 'video_capture'),
    path('attendent_results/', views.attend_result, name = 'attend_result'),
]