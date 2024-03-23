import sys, os, django, datetime
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Max
from dotenv import load_dotenv
# import wikipediaapi
import wikipedia

def my_cron_job():

    load_dotenv('../.env')
    sys.path.append(str(os.environ.get('MY_ROOT_PATH')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minordomo.settings')
    django.setup()

    import requests
    from minor_app.models import Message, Report
    from datetime import datetime

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

        # Preparing the report
        # Search the text in wikipedia
        search_results = wikipedia.search(received_text)
        report_content = ""
        if search_results:
            try:
                report_content = wikipedia.summary(search_results[0], auto_suggest=False)
            except:
                print("Error retrieving "+search_results[0])
        else:
            print("No results found for '{}'.".format(received_text))

        new_report = Report(message=new_message, content=report_content)        
        new_report.save()

        # Preparing the reply
        reply_content = "New report: <a href='"+os.environ.get('BASE_URL')+"message/"+new_message.slug+"'>"+m['message']['text']+"</a>"
        params = {
            'text': reply_content,
            'chat_id': received_user_id,
            'parse_mode': "HTML"
        }
        response = requests.post(reply_url, params=params)

my_cron_job()

