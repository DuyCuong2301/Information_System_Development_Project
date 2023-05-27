from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/management/', include(('management.urls', 'management'), namespace='management')),
]
