import os

from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseModel):
    """Класс для шифрования пакета информации (скрытия), хранящий идентификационный ключ API"""

    api_key: SecretStr = os.getenv('SITE_API', None)
    host_api: StrictStr = os.getenv('HOST_API', None)
    tg_api: SecretStr = os.getenv('TELEBOT_API', None)