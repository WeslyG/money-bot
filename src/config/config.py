from dotenv import load_dotenv
import os


class Config:
    def __init__(self):
        is_production = False
        try:
            is_production = bool(os.environ['PRODUCTION'])
        except:
            pass

        if (not is_production):
            load_dotenv()
        self.telegram_token = str(os.environ['TELEGRAM_TOKEN']) or Exception('Token not set in config')
        self.elastic_user = os.environ['ELASTIC_USER']
        self.elastic_password = os.environ['ELASTIC_PASSWORD']

