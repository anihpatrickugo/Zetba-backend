import json
from datetime import datetime
from django.db.models import signals
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


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
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S")
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





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    # print("Password reset token created for user: {}".format(reset_password_token.user.username))
    # print("Reset password token key: {}".format(reset_password_token.key)


    # send an e-mail to the user
    context = {
        # 'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token' : reset_password_token.key,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()