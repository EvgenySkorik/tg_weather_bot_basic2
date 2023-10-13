from database.common.models import db, History
from database.core import crud
from SITE_API.core import headers, site_api, url

print(url)
db_write = crud.create()
db_read = crud.retrieve()

weather = site_api.get_response()
response = weather(url, 'moscow', headers)
print(response)
data = [{'user_name': message...,'temp_now': response[0], 'temp_like_now': response[1]}]
print(data)
db_write(db, History, data)

retrieved = db_read(db, History, History.user_name, History.temp_now, History.temp_like_now)

for el in retrieved:
    print(el.temp_now, el.temp_like_now)
