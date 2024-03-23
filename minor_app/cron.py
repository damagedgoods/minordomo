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
    from minor_app.models import Message, Report
    from datetime import datetime
    reply_url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')+"/sendMessage"

    print("Starting cronjob "+str(datetime.now()))

    # Extract unread messages
    last_id = Message.objects.aggregate(Max('update_id'))
    offset = 0
    if last_id["update_id__max"] is not None:
        offset = int(last_id["update_id__max"]) + 1
    listen_url = "https://api.telegram.org/bot"+os.environ.get('TELEGRAM_TOKEN')+"/getUpdates?offset="+str(offset)    
    messages = requests.get(listen_url).json()['result']
    
    # Process each message
    for m in messages:

        received_user_id = m['message']['from']['id']
        received_text = m['message']['text']
        received_update_id = str(m['update_id'])        

        # Preparing the report. First, extract the command
        received_text_words = received_text.split()
        command = received_text_words[0].lower()
        search_text = " ".join(received_text_words[1:])
        if search_text == "":
            search_text = received_text

        new_message =  Message(text=search_text, date=timezone.now(), update_id = received_update_id)        
        print(new_message.text+" - "+str(new_message.update_id)+" - "+str(received_user_id))

        report_content = ""
        new_report = Report(message=new_message, content=report_content)     
        if command == "concept" or command == "c":
            # If it's a term, search the text in wikipedia
            print("Buscando concepto "+search_text)
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
            #print("Buscando música "+search_text)        
            new_message.category = Message.Category.MUSIC

        else:
            # If it's other, I don't know
            print("Buscando otra cosa "+search_text)        
            new_message.category = Message.Category.UNKNOWN
        
        new_message.save()
        new_report.content = report_content
        new_report.save()

        #print("Categoría: "+str(Message.Category(new_message.category).label))

        # Preparing the reply
        reply_content = "New "+Message.Category(new_message.category).label.lower()+" report: <a href='"+os.environ.get('BASE_URL')+"message/"+new_message.slug+"'>"+new_message.text+"</a>"
        params = {
            'text': reply_content,
            'chat_id': received_user_id,
            'parse_mode': "HTML"
        }
        response = requests.post(reply_url, params=params)

my_cron_job()

