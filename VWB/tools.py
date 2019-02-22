import json
from VWB import vk, tg_methods as tg
import datetime
import traceback


def log_json(data, filename):
    """Append json data to filename"""
    with open(f'VWB/logs/{filename}', 'a') as log_file:
        json.dump(data, log_file, indent=2, ensure_ascii=False)
        log_file.write('\n\n')


def log_err(e, filename):
    """Append error data to filename"""
    with open(f'VWB/logs/{filename}', 'a') as log_file:
        log_file.write(str(datetime.datetime.now()))
        log_file.write(f'\n{traceback.format_exc()}\n\n')


def init_tokens(filename):
    """ Initialize API tokens"""
    with open(filename) as token_file:
        data = json.load(token_file)
        tg.BOT_TOKEN = data['telegram']
        vk.VK_ACCESS_TOKEN = data['vk']
        print(data)
