import json
from datetime import datetime
from django.db.models import signals
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notifications


@receiver(signals.pre_save, sender=Notifications)
def send_notification(sender, instance, **kwargs):

    # check if the instance is created
    if instance.pk:
        return

    dic = {
        "title": instance.title,
        "description": instance.description,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    # turn to the data dictionary to json
    json_data = json.dumps(dic, sort_keys=True, indent=1, cls=DjangoJSONEncoder)

    # send the notification to the user
    channel_layer = get_channel_layer()
    data = str(json_data)
    async_to_sync(channel_layer.group_send)(
        str(instance.user.pk),
        {
            "type": "notify",
            "text": data,
        },
    )
