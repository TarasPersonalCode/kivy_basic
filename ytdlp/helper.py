import argparse
import json
import os
import re
import subprocess
import urllib.request, urllib

SEARCH_TEMPLATE = "https://www.youtube.com/results?search_query="
DOWNLOAD_CMD = '/home/user/.local/bin/yt-dlp https://www.youtube.com/watch?v={video_id} '\
               '{priority_choice}' \
               '-o "{output_dir}/{track_name}.%(ext)s"'

#                   video?  quality over size?
PRIORITY_CHOICES = {True:  {True:  f'-f "b" ',
                            False: f'-S "+size,+br" '},
                    False: {True:  f'-f "ba" -x --audio-format m4a ',
                            False: f'-S "+size" -x --audio-format m4a '}
                   }

RU_ALPHABET = 'абвгдеёжзийклмнопрстуфхччшщьъыэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧЧШЩЬЪЫЭЮЯ'
UA_ALPHABET = 'абвгдеєжзіиїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗІИЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'


def process_query(query_txt, video_, quality_, output_dir):
    """
        Assuming query is one of the following:
            1) copied from the browser when watching a video:
                https://www.youtube.com/watch?v={video_id}
            2) copied from the mobile app:
                https://youtu.be/{video_id}
            3) a regular en/ru/ua search query
    """
    priority_choice = PRIORITY_CHOICES[video_][quality_]
    # extension = "mp4" if video_ else "m4a"
    if query_txt.startswith('https://www.youtube.com/watch?v='):
        video_id = query_txt[32:]
    elif query_txt.startswith('https://youtu.be/'):
        video_id = query_txt[17:]
    elif query_txt.startswith('https://www.youtube.com/live/'):
        video_id = query_txt[29:].split('?')[0]
    else:
        # treating as a search query and downloading top result
        query_lower = str.lower(query_txt)
        search_query = re.sub(f'[^0-9a-zA-Z'\
                              f'{RU_ALPHABET}'\
                              f'{UA_ALPHABET}]+', 
                              '+', 
                               query_lower.replace('\n', ''))
        youtube_search_html = urllib.request.urlopen(SEARCH_TEMPLATE + urllib.parse.quote(search_query))
        video_ids = re.findall(r"watch\?v=(\S{11})", youtube_search_html.read().decode())
        # top result
        video_id = video_ids[0]
    video_name = get_name_by_id(video_id)
    print(DOWNLOAD_CMD.format(
                                    video_id=video_id,
                                    track_name=video_name,
                                    # extension=extension,
                                    priority_choice=priority_choice,
                                    output_dir=output_dir))
    subprocess.check_output(DOWNLOAD_CMD.format(
                                    video_id=video_id, 
                                    track_name=video_name,
                                    # extension=extension,
                                    priority_choice=priority_choice,
                                    output_dir=output_dir), shell=True)
    extension = get_extension(video_name, output_dir)
    print(extension)
    return f'{video_name}.{extension}'

def get_extension(track_name, output_dir):
    fnames = [fname for fname in os.listdir(output_dir) if fname.startswith(track_name)]
    fnames_modified = {fname: os.path.getmtime(f'{output_dir}/{fname}') for fname in fnames}
    recent = list(fnames_modified.keys())[0]
    for key in fnames_modified:
        if fnames_modified[key] > fnames_modified[recent]:
            recent = key
    return key.split('.')[-1]

def get_name_by_id(video_id_):
    import requests
    from bs4 import BeautifulSoup
    s = BeautifulSoup(requests.get(f"https://www.youtube.com/watch?v={video_id_}").text, "html.parser")
    try:
        video_name = s.text.split('YouTubeAboutPress')[0][:-3]
        channel_name = str(s).split('channelName')[1][:100].split('"')[2]
    except:
        try:
            video_name = str(s).split('</title><meta content=')[0].split('<title>')[-1]
            channel_name = 'cantclassify'
        except:
            import uuid
            video_name = uuid.uuid4().hex
            channel_name = '000'
    return re.sub(f'[^0-9a-zA-Z'\
                  f'{RU_ALPHABET}'\
                  f'{UA_ALPHABET}]+', 
                  '.', 
                  f'{video_name}.{channel_name}')
