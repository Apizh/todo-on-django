from django.contrib import admin
from django.urls import path, include
from todo_home.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo_home.urls')),  # Include the shop app's URL configuration'
]

handler404 = page_not_found
