from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('todo_home.urls')),  # Include the shop app's URL configuration'
]