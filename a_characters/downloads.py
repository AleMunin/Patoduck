from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django import forms 
from django.forms import ModelForm 

from .models import *
from .forms import *
from .tools import *

import json, io, zipfile
from django.http import JsonResponse, HttpResponse



# this one is not registered, but have tested them before
def download_conv_only(request):

    queryset = Conversation.objects.all()
    data = list(queryset.values())

    json_data = json.dumps(data, indent=4, sort_keys=True, default=str)

    response = HttpResponse(
        json_data, 
        content_type='application/json'
        )
    response['Content-Disposition'] = 'attachment; filename="data.json"'

    
    return response


def download_all_flat(request): #json dumps individually. Does not make formats nice like names instead of id-keys and so on

    all_convs = Conversation.objects.all()
    #data = list(convs.values())

    all_json = []
    buffer = io.BytesIO() # will hold file in memory

    for conv in all_convs:
        conv_json = []
        speech_count = 0

        conv_json.append(f"{conv.title}/000--(CONV)--{conv.title}.json")
        conv_json.append(json.dumps(conv.__dict__, indent=4, sort_keys=True, default=str))

        speeches = Speech.objects.filter(conversation=conv.id)

        if not speeches:    #if there are no speeches, we skip saving the conv to json.
            continue

        all_json.append(conv_json)


        for speech in speeches:

            speech_json = []
            if speech.is_first is True:
                file_name = f"000--(START)--{speech.name}"
            elif speech.has_fork:

                file_name = f"0{speech_count}--(FORKS)--{speech.name}"
            else:
                file_name = f"0{speech_count}--{speech.name}"
            
            speech_count += 1

            file_path = f'{conv.title}/{file_name}.json'
            #sanitize dialogue here
            # json dump

            speech_json.append(file_path)
            speech_json.append(json.dumps(speech.__dict__, indent=4, sort_keys=True, default=str))
            
            all_json.append(speech_json)

    with zipfile.ZipFile(buffer,'w') as zip:
        for json_dict in all_json:
            zip.writestr(json_dict[0],json_dict[1])

    buffer.seek(0)

    #json_data = json.dumps(data, indent=4, sort_keys=True, default=str)

    response = HttpResponse(
        buffer, 
        content_type='application/zip'
        )
    response['Content-Disposition'] = 'attachment; filename="all_conv.zip"'

    
    return response

# ----------------- REGISTERED IN URLS

def download_all(request):

    all_convs = Conversation.objects.all()
    #data = list(convs.values())

    all_json = []
    buffer = io.BytesIO() # will hold file in memory

    for conv in all_convs:
        conv_json = []
        speech_count = 0

        conv_json.append(f"{conv.title}/000--(CONV)--{conv.title}.json")
        conv_json.append(json.dumps(conv.__dict__, indent=4, sort_keys=True, default=str))

        speeches = Speech.objects.filter(conversation=conv.id)

        if not speeches:    #if there are no speeches, we skip saving the conv to json.
            continue

        all_json.append(conv_json)


        for speech in speeches:

            speech_json = []
            if speech.is_first is True:
                file_name = f"000--(DIA)(START)--{speech.name}"
            elif speech.has_fork:

                file_name = f"0{speech_count}--(DIA)(FORKS)--{speech.name}"
            else:
                file_name = f"0{speech_count}--(DIA)--{speech.name}"
            
            speech_count += 1

            file_path = f'{conv.title}/{file_name}.json'
            #sanitize dialogue here
            
            to_json = speech.__dict__
            fork_fields = get_fork_fields(speech,"ids")
            
            # I know I know, i could get them all in a single query, i'll deal with it later.

            to_json['speaker_en'] = Character.objects.filter(id=speech.speaker).values_list("name")
            to_json['speaker_pt'] = Character.objects.filter(id=speech.speaker).values_list("name_pt")
            to_json['speaker_es'] = Character.objects.filter(id=speech.speaker).values_list("name_es")


            to_json['next_speech'] = Speech.objects.filter(id=speech.next_speech).values_list("name")
            to_json['previous_speech'] = Speech.objects.filter(id=speech.previous_speech).values_list("name")

            for key,field in fork_fields.items():
                if field is None:
                    continue
                to_json[key] = Speech.objects.filter(id=field).values_list("name")

            
            # json dump

            speech_json.append(file_path)
            speech_json.append(json.dumps(to_json, indent=4, sort_keys=True, default=str))

            
            all_json.append(speech_json)

    with zipfile.ZipFile(buffer,'w') as zip:
        for json_dict in all_json:
            zip.writestr(json_dict[0],json_dict[1])

    buffer.seek(0)

    #json_data = json.dumps(data, indent=4, sort_keys=True, default=str)

    response = HttpResponse(
        buffer, 
        content_type='application/zip'
        )
    response['Content-Disposition'] = 'attachment; filename="all_conv.zip"'

    
    return response

