import os
from django.conf import settings
from slack import WebClient

from witch import PROJECT_NAME

_ALERTS_CHANNEL = '#alerts'

class SlackError(Exception):
    pass

def send(message, channel=_ALERTS_CHANNEL):   
    client = WebClient(token=settings.SLACK_TOKEN) 
    response = client.chat_postMessage(
        text=f'*{PROJECT_NAME}* {message}',
        channel=channel
    )
    if not response.get('ok', False):
        raise SlackError(response)
    return response