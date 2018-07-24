import requests
import json
import vk
import io
import tools


BOT_TOKEN = '556191721:AAH11vENmvGlnHlDKnGiwWCnIIIdW5v-ntA'

BASE_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'


def handleUpdate(update):
    chat_id = update['message']['chat']['id']
    try:
        message_text = update['message']['text']
    except KeyError:
        return 'KeyError: \'text\''
    returned_messages = []
    rm = 'None'
    if message_text == '/start':
        rm = send_message(chat_id, u'🔪')
    elif message_text == '/help':
        rm = send_message(chat_id, 'no')
    elif message_text == 'pt':
        rm = send_photo(chat_id, 'https://pp.userapi.com//c626516//v626516637//57203//pCdItq4XreQ.jpg')
        returned_messages.append(rm)
        rm = send_message(chat_id, 'Мик Гордон подтвердил, что саундтрек DOOM Eternal будет иметь тот же стиль, что у перезапуска.\n\n\"Мы потратили очень много времени, чтобы определить звук DOOM, и мы не собираемся отказываться от него\"\n\nГотовьте свои ушки!', 'https://vk.com/dev/objects/post', 'VK link')
    elif message_text == 'ptg':
        rm = send_photo(chat_id, 'https://pp.userapi.com//c626516//v626516637//57203//pCdItq4XreQ.jpg', 'https://vk.com/dev/objects/post', 'VK link', 'Мик Гордон подтвердил, что саундтрек DOOM Eternal будет иметь тот же стиль, что у перезапуска.')
    elif message_text == 'sa':
        rm = send_audio(chat_id, 'https://cs9-17v4.vkuseraudio.net/p5/6914a6d0d82c38.mp3')
    returned_messages.append(rm)
    tools.log_json(returned_messages, 'post_replies.log')


def send_message(chat_id, text, inline_url=None, inline_text=None):
    message = {'chat_id': chat_id, 'text': text}
    if inline_url != None and inline_text != None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendMessage', message)


def send_photo(chat_id, photo, inline_url=None, inline_text=None, caption=''):
    message = {'chat_id': chat_id, 'photo': photo, 'caption': caption}
    if inline_url != None and inline_text != None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendPhoto', message)


def send_media_group(chat_id, media):
    message = {'chat_id': chat_id, 'media': media}
    return make_request('sendMediaGroup', message)


def send_audio(chat_id, audio_url, performer='Unknown', title='Unknown'):
    url = '{}sendAudio?chat_id={}&performer={}&title={}'.format(BASE_URL, chat_id, performer, title)
    remote_file = requests.get(audio_url)
    file1 = io.BytesIO(remote_file.content)
    files = dict({'audio': file1})
    post = requests.post(url, files=files)
    return post.json()


def make_request(method, message):
    url = BASE_URL + method
    post = requests.post(url, json=message)
    return post.json()


def append_inline_link(message, inline_url, inline_text):
    ikb = {'text': inline_text, 'url': inline_url}
    ikm = {'inline_keyboard': [[ikb]]}
    message['reply_markup'] = ikm
    return message


