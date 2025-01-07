

# 1. Get query of ALL conversations
#   1.1 for each query, get all speeches that point to this conv.
#   1.2 sort them by finding the first one.
#   1.3 create a folder for the quest.
#   1.5 Convert all the characters from the database to yarn-friendly.
#   1.6 Create a json object for every speech.
#       1.6.1 Maybe for fork field, for good measure, have a list with all the names at the query.
#       1.7 Create a json object for the conversation.
# 2. Separate where quests and single convs are stored.

# 3. dump all the hierarchy and json files into a zip.
#   3.1 You might want to add some metadata of when this happened.
# 4. Make it downloadable.

from .models import *


def get_speeches(conv):
    print("")

def get_conv():
    all_conv = Conversation.objects.all()
    conv_count = 0
    total_speech_count = 0

    for conv in all_conv:
        conv_count += 1
        speech_count = 0
        speeches = Speech.objects.filter(conversation=conv.id)
        
        

