import sys, os, django, datetime
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Max
from dotenv import load_dotenv
import wikipedia

def my_cron_job():

    # Setup & configuration
    load_dotenv('../.env')
    sys.path.append(str(os.environ.get('MY_ROOT_PATH')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minordomo.settings')
    django.setup()
    import requests
    from minor_app.models import Message, Report, Variable
    from datetime import datetime

    # Extract unread messages
    last_id_results = Variable.objects.filter(name="LAST_ID")
    if not last_id_results:
        last_id_obj =  Variable(name="LAST_ID", value=None)
    else:
        last_id_obj = last_id_results[0]
    offset = 0
    if last_id_obj.value is not None:
        offset = int(last_id_obj.value) + 1

    telegram_api_url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')
    telegram_listen_url = telegram_api_url+"/getUpdates?offset="+str(offset)    
    telegram_reply_url = telegram_api_url+"/sendMessage"
    messages = requests.get(telegram_listen_url).json()['result']
    
    # Process each message
    for m in messages:

        received_user_id = m['message']['from']['id']
        received_text = m['message']['text']
        received_update_id = str(m['update_id'])        
        params = {
            'chat_id': received_user_id,
            'parse_mode': "HTML"
        }

        # Preparing the report. First, extract the command
        received_text_words = received_text.split()
        command = received_text_words[0].lower()
        search_text = " ".join(received_text_words[1:])
        if search_text == "":
            search_text = received_text

        # Updating the global id, to mark the message as processed
        last_id_obj.value = received_update_id
        last_id_obj.save()

        # If the term exists, answer and finish processing this message
        existing = False
        if Message.objects.filter(text=search_text):
            params["text"] = search_text+" already exists, it won't be saved again."
            response = requests.post(telegram_reply_url, params=params)
            continue

        new_message =  Message(text=search_text, date=timezone.now(), update_id = received_update_id)        
        print(new_message.text+" - "+str(new_message.update_id)+" - "+str(received_user_id))

        # Generating the report depending on the command
        report_content = ""
        new_report = Report(message=new_message, content=report_content)     
        if command == "concept" or command == "c":
            # If it's a term, search the text in wikipedia
            search_results = wikipedia.search(search_text)            
            if search_results:
                try:
                    report_content = wikipedia.summary(search_results[0], auto_suggest=False)
                except:
                    print("Error retrieving "+search_results[0])
            else:
                print("No results found for '{}'.".format(received_text))
            new_message.category = Message.Category.CONCEPT
        elif command == "music" or command == "m":
            # If it's music, search spotify
            new_message.category = Message.Category.MUSIC
        else:
            # If it's other, I don't know
            new_message.category = Message.Category.UNKNOWN
        
        new_message.save()
        new_report.content = report_content
        new_report.save()

        # Replying
        reply_content = "New "+Message.Category(new_message.category).label.lower()+" report: <a href='"+os.environ.get('BASE_URL')+"message/"+new_message.slug+"'>"+new_message.text+"</a>"
        params["text"] = reply_content,
        response = requests.post(telegram_reply_url, params=params)

my_cron_job()

