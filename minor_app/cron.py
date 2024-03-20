import sys, os, django, datetime
from django.utils import timezone
from django.db.models import Max
from dotenv import load_dotenv

sys.path.append('/Users/diegocano/workspace/minordomo/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minordomo.settings')
django.setup()

import requests
from minor_app.models import Message
from datetime import datetime

def my_cron_job():

    print("Starting cronjob "+str(datetime.now()))

    last_id = Message.objects.aggregate(Max('update_id'))
    offset = 0
    if last_id["update_id__max"] is not None:
        offset = int(last_id["update_id__max"]) + 1

    listen_url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')+"/getUpdates?offset="+str(offset)    
    response = requests.get(listen_url)
    response_json = response.json()
    messages = response_json['result']    

    reply_url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')+"/sendMessage"
    for m in messages:        
        received_user_id = m['message']['from']['id']
        received_text = m['message']['text']
        received_update_id = str(m['update_id'])
        print(received_text+" - "+str(received_update_id)+" - "+str(received_user_id))
        new_message =  Message(text=received_text, date=timezone.now(), update_id = received_update_id)
        new_message.save()
        params = {
            'text': "Noted \'"+m['message']['text']+"\'",
            'chat_id': received_user_id
        }
        response = requests.post(reply_url, params=params)

my_cron_job()

