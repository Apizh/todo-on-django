from django.urls import path

from todo_home.views import home, login, signup

app_name = 'todo_home'

urlpatterns = [
    path('', home, name='home_page'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
]
