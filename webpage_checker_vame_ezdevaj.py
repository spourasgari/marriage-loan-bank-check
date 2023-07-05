# Please check and modify the code and documentations before using

from time import sleep
from bs4 import BeautifulSoup
import requests
telegram_token = '****************************' #Replace the asterisks with your Telegram bot token
chat_id = 12345678 #Replace your telegram chat ID (This is a telgram bot to get it quickly: @get_id_bot)

# I will add a timeout to the request function later. Take care.
class TelegramSender():
    def write(self, bot_message):
        url = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text=<b>{bot_message}</b>'
        requests.get(url)

telegarm_sender = TelegramSender()

# These are the example links from the only website that I found. You can find the required parameters p1 and p2

# mellat_tehran = "https://vam.kandoocn.com/which-banks-is-open?bank=12&province=24"
# pasargad_tehran = "https://vam.kandoocn.com/which-banks-is-open?bank=57&province=24"
# tejarat_gilan = "https://vam.kandoocn.com/which-banks-is-open?bank=18&province=02"
# General Template = "https://vam.kandoocn.com/which-banks-is-open?bank=p1&province=p2"
# Main address: https://vam.kandoocn.com/which-banks-is-open
# Add your desired banks' list as below:

desired_banks = [('12','24','**** Mellat - Tehran ****'),('57','24','**** Pasargar - Tehran ****'),('18','02','**** Tejarat - Gilan ****')]

def get_link(p1,p2):
    resp = requests.get(f"https://vam.kandoocn.com/which-banks-is-open?bank={p1}&province={p2}").text
    return resp

# Here, we check where the website shows the last active day of that bank

def get_status(p1,p2):
    html = get_link(p1,p2)
    soup = BeautifulSoup(html, "html.parser")
    p = soup.body.select('#home > div:nth-child(5) > div.d-table > div > div > div > div > table > tbody > tr > td:nth-child(2) > a')[0]
    return p.contents[0]


def send_telegram_notification(message):
    print(message)
    telegarm_sender.write(message)

    
# Here, we check the banks' status every 300 seconds, and send a heartbeat notification every 6 hours.
# We assume that depending on code's start time, the day will change after 12 hours. It is written in this way for safety and definitely can be improved

heart_beat_counter = 0
day_break = []
half_day_indicator = 0
sleep_time = 300
heart_beat_hours = 6

send_telegram_notification("Loop Started...")

while 1:
    heart_beat_counter = heart_beat_counter + 1
    
    if half_day_indicator == 2:
        day_break = []
        half_day_indicator = 0
        
    if heart_beat_counter == 3600*heart_beat_hours/sleep_time:
        heart_beat_counter = 0
        half_day_indicator += 1
        send_telegram_notification("S  t  i  l  l    A  l  i  v  e")
        
    for (p1,p2,p3) in desired_banks:
        if not(p3 in day_break):
            status = get_status(p1,p2)
            if status == "امروز":
                send_telegram_notification(p3)
                day_break.append(p3)
            
    sleep(sleep_time)
