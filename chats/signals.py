
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_presence.signals import presence_changed
from django.dispatch import receiver

from django.db.models.signals import post_save
#from .models import ChatMember


#@receiver(post_save, sender=ChatMember)
#def post_save_member(sender, instance, **kwargs):
#    if kwargs['created']:
#        print(f'В чат "{instance.chat}" добавлен пользователь {instance}!')
#    else:
#        print(f'В чате "{instance.chat}" изменены данные пользователя {instance}!')#


channel_layer = get_channel_layer()

@receiver(presence_changed)
def broadcast_presence(sender, room, **kwargs):
    """
    Broadcast the new list of present users to the room.
    """

    message = {
      "type": "presence",
      "payload": {
          "channel_name": room.channel_name,
          "members": [user.serialize() for user in room.get_users()],
          "lurkers": room.get_anonymous_count(),
      }
    }

    # Prepare a dict for use as a channel layer message. Here, we're using
    # the type "forward.message", which will magically dispatch to the
    # channel consumer as a call to the `forward_message` method.
    channel_layer_message = {
        "type": "forward.message",
        "message": json.dumps(message)
    }
    print('****************************************************')
    async_to_sync(channel_layer.group_send)(room.channel_name, channel_layer_message)

