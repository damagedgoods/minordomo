import requests

def my_cron_job():
    url = "https://api.telegram.org/bot6819497556:AAGcgaZv6Fbyritjq6SyGLSgHWw-QseBfck/getUpdates"
    response = requests.get(url)
    response_json = response.json()
    print(response_json)
    messages = response_json['result']
    for m in messages:
        print(m['message']['text'])

my_cron_job()

