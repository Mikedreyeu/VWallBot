import requests
import re
from VWB import bot, tools
import time


VK_ACCESS_TOKEN = ''
VK_BASE_URL = 'https://api.vk.com/method/'


class Post:
    """VK post class."""
    def __init__(self, group_name=None, id_=None, text=None, link=None,
                 attached_link=None, photos=None, videos=None, docs=None,
                 has_audio=False, has_album=False, has_photo_list=False,
                 page=None):
        self.group_name = group_name
        self.id = id_
        self.text = text
        self.link = link
        self.attached_link = attached_link
        self.photos = photos
        self.videos = videos
        self.docs = docs
        self.has_audio = has_audio
        self.has_album = has_album
        self.has_photo_list = has_photo_list
        self.page = page
        if photos is None:
            self.photos = []
        if videos is None:
            self.videos = []
        if docs is None:
            self.docs = []


def get_posts(start_time=None):
    """
    Return list of Post objects

    Args:
    start_time -- Identifier required to get the next page of results
    """
    posts = newsfeed_get(start_time)
    if len(posts['response']['items']) > 0:
        bot.set_start_time(posts['response']['items'][0]['date'])
        return parse_posts(posts)
    return []


def newsfeed_get(start_time=None, filters='post'):
    """
    Return data required to show newsfeed for the current user.

    Args:
    filters -- Listed comma-separated list of feed lists that you need to
               receive
    start_time -- Earliest timestamp (in Unix time) of a news item to return
    """
    url = (f'{VK_BASE_URL}newsfeed.get?filters={filters}' +
           f'&start_time={start_time}&return_banned=0' +
           f'&access_token={VK_ACCESS_TOKEN}&v=5.80')
    posts = requests.get(url)
    return posts.json()


def parse_posts(posts):
    """
    Return list of Post objects

    Args:
    posts -- VK API newsfeed.get method response
    """
    parsed_posts = []
    for item in posts['response']['items']:
        post = Post()
        post.id = item['post_id']
        source_id = item['source_id']
        if source_id < 0:
            post.group_name = get_group_name(abs(source_id))
        else:
            post.group_name = get_user_name(source_id)
        post.text = item['text']
        post.link = f'https://vk.com/wall{item["source_id"]}_{post.id}'
        if 'attachments' in item:
            parse_attachments(item, post)
        parsed_posts.append(post)
        time.sleep(0.33)  # [VK API]: 5 requests per second(get_group_name)
    return parsed_posts


def parse_attachments(item, post):
    """
    Appends attachments to the Post object

    Args:
    item -- Post from VK API newsfeed.get method response
    post -- Post object
    """
    videos_count = len(
        [attach for attach in item['attachments'] if attach['type'] == 'video']
    )
    delay_video_requests = True if videos_count > 3 else False

    for attachment in item['attachments']:
        if attachment['type'] == 'photo':
            for size in reversed(attachment['photo']['sizes']):
                if (size['type'] == 'z' or size['type'] == 'y' or
                        size['type'] == 'x' or size['type'] == 'm' or
                        size['type'] == 's'):
                    post.photos.append(size['url'])
                    break
        elif attachment['type'] == 'video':
            post.videos.append(
                parse_video(attachment['video'], delay_video_requests)
            )
        elif attachment['type'] == 'doc' and attachment['doc']['size'] < 10**7:
            post.docs.append(attachment['doc']['url'])
        elif attachment['type'] == 'link':
            post.attached_link = attachment['link']['url']
        elif attachment['type'] == 'page':
            post.page = attachment['page']['view_url']
        elif attachment['type'] == 'audio':
            post.has_audio = True
        elif attachment['type'] == 'album':
            post.has_album = True
        elif attachment['type'] == 'photos_list':
            post.has_photos_list = True


def parse_video(video, delay_video_requests=False):
    """
    Return video url from VK video object.

    Args:
    video -- VK video object
    """
    url = (f'{VK_BASE_URL}video.get?owner_id={video["owner_id"]}' +
           f'&videos={video["owner_id"]}_{video["id"]}_{video["access_key"]}' +
           f'&count=1&extended=0&v=5.80&access_token={VK_ACCESS_TOKEN}')

    if delay_video_requests:
        time.sleep(0.5)

    try:
        video_obj = requests.get(url).json()['response']['items'][0]
    except KeyError as e:
        tools.log_err(e, 'errors.log')
        return '[FAILED TO GET VIDEO URL]'

    video_url = video_obj['player']
    try:
        video_platform = video_obj['platform'].lower()
    except KeyError:
        video_url = (f'https://vk.com/video{video_obj["owner_id"]}' +
                     f'_{video_obj["id"]}')
        return video_url
    if video_platform == 'youtube':
        watch_v = re.search(r'\/([^\/]+)\?', video_url).group(1)
        video_url = f'https://www.youtube.com/watch?v={watch_v}'
    elif video_platform == 'vimeo':
        vimeo_video_id = re.search(r'\/([^\/]+)\?', video_url).group(1)
        video_url = f'https://vimeo.com/{vimeo_video_id}'
    return video_url


def get_group_name(group_id):
    """
    Return group by id.

    Args:
    group_id -- VK group ID
    """
    url = (f'{VK_BASE_URL}groups.getById?group_id={group_id}' +
           f'&access_token={VK_ACCESS_TOKEN}&v=5.80')
    group = requests.get(url)
    return group.json()['response'][0]['name']


def get_user_name(user_id: int):
    """
    Return user by id.

    Args:
    user_id -- VK user ID
    """
    url = (f'{VK_BASE_URL}users.get?users_id={user_id}' +
           f'&fields=nickname,screen_name' +
           f'&access_token={VK_ACCESS_TOKEN}&v=5.80')
    group = requests.get(url)
    response = group.json()['response'][0]
    full_name = f'{response["first_name"]} {response["last_name"]}'
    return full_name
