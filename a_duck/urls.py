"""
URL configuration for a_duck project.

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

from a_characters.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

    path('char', character_create_view, name='create_char'),
    path('all-chars', all_char_view, name="all_char"),

    path('location', location_create_view, name="create_location"),
    path('all-loc', all_location_view, name="all_location"), 

    path('quest', quest_create_view, name='create_quest'),
    path('all-quests', all_quest_view, name='all_quest'),


    path('conv', conversation_create_view, name='create_conv'),
    path('all-conv', all_conv_view, name='all_conv'),
    path('edit_conv/<pk>/', edit_conv_view, name='edit_conv'), # use /<pk> on this

    #non pages, just htmx snippets

    #non pages, but redirecting functions

    path('speech-sent/<pk>/', create_speech_process, name='create_speech'),

    
    path('get-fork-question/<speech_pk>/', get_fork_question, name='get_fork_form'),
    path('save-fork-question/<speech_pk>/', fork_question_process, name='create_fork'),

    # Download json -----------------------------------------------

    path('downall', download_all, name='downall')
]

