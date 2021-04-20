from . import views as user_views
from django.urls import path

urlpatterns = [

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),

]