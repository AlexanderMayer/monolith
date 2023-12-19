from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('profile/<int:pk>', Profile.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:user_id>', delete, name='delete'),
    path('update/<int:pk>', UserView.as_view(), name='update'),
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('create/', create_post, name='create'),
    path('voted/<int:pk>', VotedView.as_view(), name='voted'),
    path('polls', PollsList.as_view(), name='polls_list'),
]
