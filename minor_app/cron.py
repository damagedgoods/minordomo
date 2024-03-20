import sys, os, django, datetime
from django.utils import timezone
from django.db.models import Max
from dotenv import load_dotenv

sys.path.append('/Users/diegocano/workspace/minordomo/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minordomo.settings')
django.setup()

import requests
from minor_app.models import Message

def my_cron_job():

    # Mirar el último leído
    last_id = Message.objects.aggregate(Max('update_id'))
    offset = 0
    if last_id["update_id__max"] is not None:
        offset = int(last_id["update_id__max"]) + 1

    # Construir la llamada con el offset adecuado
    url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')+"/getUpdates?offset="+str(offset)
    
    response = requests.get(url)
    response_json = response.json()
    messages = response_json['result']

    # Grabar los mensajes en la base de datos
    for m in messages:
        print(m['message']['text']+" - "+str(m['update_id']))
        new_message =  Message(text=m['message']['text'], date=timezone.now(), update_id = str(m['update_id']))
        new_message.save()

    # Procesar cada mensaje
        
    # Responder
    url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')+"/sendMessage"
    params = {
        'text': "text",
        'chat_id': "@MinordomoBot"
    }
    response = requests.post(url, params=params)

my_cron_job()

