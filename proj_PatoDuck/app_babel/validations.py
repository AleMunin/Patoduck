def break_conv(conv_pk):
    conv = get_object_or_404(Conversation,id=conv_pk)
    conv.broken_chain = True
    conv.save()