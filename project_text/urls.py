from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('text_app.urls')),
    path('', include('users.urls'))
]
