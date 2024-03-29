import requests
import io
from VWB import tools


BOT_TOKEN = ''

BASE_URL = 'https://api.telegram.org/bot'


def make_request(method, message):
    """
    Make a query to the Telegram Bot API.

    Args:
    method -- Method name
    message -- json to send
    """
    url = f'{BASE_URL}{BOT_TOKEN}/{method}'
    post = requests.post(url, json=message)
    return post.json()


def append_inline_link(message, inline_url, inline_text):
    """
    Append inline link to the message.

    Args:
    message -- The message
    inline_url -- URL link
    inline_text -- Text in URL button
    """
    ikb = {'text': inline_text, 'url': inline_url}
    ikm = {'inline_keyboard': [[ikb]]}
    message['reply_markup'] = ikm
    return message


"""Down below are Bot API methods"""


def send_message(chat_id, text, inline_url=None,
                 inline_text='VK link', html=True):
    message = {'chat_id': chat_id, 'text': text}
    if html is True:
        message['parse_mode'] = 'HTML'
    if inline_url is not None and inline_text is not None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendMessage', message)


def send_photo(chat_id, photo, caption='',
               inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id,
               'caption': caption, 'photo': photo, 'parse_mode': 'HTML'}
    if inline_url is not None and inline_text is not None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendPhoto', message)


def send_video(chat_id, video, caption='',
               inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id, 'video': video,
               'caption': caption, 'parse_mode': 'HTML'}
    if inline_url is not None and inline_text is not None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendVideo', message)


def send_media_group(chat_id, media):
    message = {'chat_id': chat_id, 'media': media}
    return make_request('sendMediaGroup', message)


def send_document(chat_id, document, caption='',
                  inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id, 'document': document,
               'caption': caption, 'parse_mode': 'HTML'}
    if inline_url is not None and inline_text is not None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendDocument', message)


def send_audio(chat_id, audio_url, performer='Unknown', title='Unknown'):
    url = (f'{BASE_URL}sendAudio?chat_id={chat_id}' +
           f'&performer={performer}&title={title}')
    remote_file = requests.get(audio_url)
    file1 = io.BytesIO(remote_file.content)
    files = dict({'audio': file1})
    post = requests.post(url, files=files)
    return post.json()
