import json
import requests
import telebot
from settings import SiteSettings
site = SiteSettings()


bot = telebot.TeleBot('6351189777:AAFlSX8Yfd-6RSQD1SVhM1cRKiHfTFrvdC0')
URL = 'https://open-weather13.p.rapidapi.com/city/'
headers = {
    "X-RapidAPI-Key": site.api_key,
    "X-RapidAPI-Host": site.host_api
}


res = requests.get(URL + 'moscow', headers=headers)
data = json.loads(res.text)
print(data)
