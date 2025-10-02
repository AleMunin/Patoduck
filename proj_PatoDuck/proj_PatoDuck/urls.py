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
from app_babel.views_htmx import *

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
    path('create/quest', quest_create_view, name='create_quest'),
    path('create/loc', location_create_view, name="create_location"),
    path('create/conv', conversation_create_view, name='create_conv'),
    
    
    path('create/speech/<conv_pk>', speech_create_view, name='create_speech'),
    path('create/speech/<reply_to_pk>', reply_create_view, name='create_reply'),
    # Edit Forms
    
    path('edit/conv/<pk>', edit_conv_view, name='edit_conv' ), #? Remember that this will create speeches too
    path('edit/speech/<speech_pk>', edit_speech_view, name='edit_speech'), #? HTMX


    # HTMX requests
    
    path('forms/new_speech/<conv_pk>', htmx_get_new_speech_form, name = 'get_speech_form'),
    path('forms/edit_speech/<speech_pk>', htmx_get_edit_speech_form, name = 'get_speech_edit_form'),
    path('forms/new_reply/<reply_to_pk>', htmx_get_new_reply_form, name = 'get_speech_reply_form')




]
