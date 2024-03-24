
from django.contrib import admin
from django.urls import path, include

from employers.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
]
