import environ
import requests


env = environ.Env()
environ.Env.read_env()

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN = env('BOT_TOKEN')
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
CAT_TEXT_ERR = 'Не знаю, о чём ты, но вот тебе кот!'
CAT_REMAIND_TEXT = ''
MAX_COUNTER = 10000000000
units = {'ч': ('ч', 'час', 'часы', 'часов', 'часа'),
         'с': ('с', 'c', 'сек', 'секунд', 'секунды', 'секунда'),
         'м': ('м', 'мин', 'минут', 'минуты', 'минута'),
         'д': ('дня', 'дней', 'дни', 'д', 'день')}

offset = -2
counter = 0
cat_response: requests.Response
chat_id: int | str
text: str
pattren: str
questions_dic: dict
time_units: dict = {'с': ('с', 1),
                    'м': ('м', 60),
                    'ч': ('ч', 3600),
                    'д': ('д', 3600 * 24)}

tasks_dict: dict = {}