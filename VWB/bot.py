from VWB import vk, tg_methods as tg
import time


def set_start_time(next_from):  # tmp func
    with open('VWB/start_time_tmp.txt', 'w') as f:
        f.write(str(int(next_from) + 1))


def get_start_time():  # tmp func
    with open('VWB/start_time_tmp.txt', 'r') as f:
        return f.read()


def start_bot():
    tmp_chat_id = '-1001391410629'
    while True:
        start_time = get_start_time()
        if start_time == '':
            start_time = int(time.time() - 100)
            set_start_time(start_time)
        posts = vk.get_posts(start_time)
        if len(posts) != 0:
            send_posts(tmp_chat_id, posts)
        time.sleep(300)


def handle_update(update):
    try:
        chat_id = update['message']['chat']['id']
        message_text = update['message']['text']
    except KeyError:
        return
    if message_text == '/start':
        tg.send_message(chat_id, '🔪')
    elif message_text == '/help':
        tg.send_message(chat_id, 'no')


def send_posts(chat_id, posts):
    for post in reversed(posts):
        docs_count = len(post.docs)
        photos_count = len(post.photos)
        text = post.text
        text = '<b>{}</b>\n'.format(post.group_name) + text

        if post.attached_link is not None:
            text += '\n' + post.attached_link
        if post.page is not None:
            text += '\n' + post.page
        if post.has_album is True:
            text += '\n[VWallBot: VK Album]'
        if post.has_photo_list is True:
            text += '\n[VWallBot: VK Photo List]'
        if post.has_audio is True:
            text += '\n[VWallBot: VK Audio]'

        for video in post.videos:
            text += '\n' + video

        if docs_count == 1 and photos_count == 0:
            tg.send_document(chat_id, post.docs[0], text, post.link)
        elif docs_count > 1 and photos_count == 0:
            for doc in post.docs:
                tg.send_document(chat_id, doc)
            tg.send_message(chat_id, text, post.link)

        elif photos_count == 1 and docs_count == 0:
            tg.send_photo(chat_id, post.photos[0], text, post.link)
        elif photos_count > 1 and docs_count == 0:
            tg.send_media_group(chat_id, convert_to_im(post.photos, 'photo'))
            tg.send_message(chat_id, text, post.link)

        elif photos_count >= 1 and docs_count >= 1:
            tg.send_photo(chat_id, post.photos[0])
            for doc in post.docs:
                tg.send_document(chat_id, doc)
            tg.send_message(chat_id, text, post.link)

        elif photos_count == 0 and docs_count == 0:
            tg.send_message(chat_id, text, post.link)


def convert_to_im(array, im_type):
    input_media = []
    for media in array:
        input_media.append({'type': im_type, 'media': media})
    return input_media
