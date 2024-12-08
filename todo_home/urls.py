from django.urls import path

from todo_home.views import home, login, signup, add_todo, signout, delete_todo

app_name = 'todo_home'

urlpatterns = [
    path('', home, name='home_page'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('add_todo/', add_todo, name='add_todo'),
    path('logout/', signout, name='signout'),
    path("delete_todo/<int:id>", delete_todo, name="delete_todo"),
]
