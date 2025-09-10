"""
URL configuration for proj_PatoDuck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app_babel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    # Main Overviews
    
    path('', home_view),
    path('all/chars', all_char_view, name="all_char"),
    path('all/locs', all_location_view, name="all_location"), 
    path('all/quests', all_quest_view, name='all_quest'),
    path('all/convs', all_conv_view, name='all_conv'),
    
    
    # Creation Forms
    path('create/char', character_create_view, name='create_char'),

]
