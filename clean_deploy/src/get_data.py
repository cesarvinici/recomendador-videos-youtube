import requests as rq
import bs4 as bs4
import re
import time
import youtube_dl 
import asyncio
from requests_html import HTMLSession, AsyncHTMLSession

def download_search_page(query, page):
    url = "https://www.youtube.com/results?search_query={query}&sp=CAI%253D&p={page}"
    urll = url.format(query=query, page=page)
    session = HTMLSession()
    # enviado requisição para o youtube
    response = session.get(urll)
    # executando Java-script
    # t = Thread(target=render_html)
    response.html.render(sleep=1)

    return response.html.html


def download_video_page(link):
    url = "https://www.youtube.com{link}"
    urll = url.format(link=link)
    response = rq.get(urll)
    
    link_name = re.search("v=(.*)", link).group(1)

    return response.text


def parse_search_page(page_html):
     # Processando a página html
    parsed = bs4.BeautifulSoup(page_html, "html.parser")

    video_list = []
     # Buscando todas as tags "a" com o id "video-title"
    ancors = parsed.find_all('a', attrs={"id": "video-title"})
    for e in ancors:
        link = e['href']
        title = e['title']
        data = {"link": link, "title": title}
        video_list.append(data)
    
    return video_list

def parse_video_page(video_link):
    URL = "https://www.youtube.com{link}"
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, 'verbose':False})
    try:
        r = ydl.extract_info(url=URL.format(link=video_link), download=False)
        year = r['upload_date'][:4]
        month = r['upload_date'][4:6]
        day = r['upload_date'][6:]
    except Exception:
        return False
    
    video_info = {
        'uploader': r['uploader'],
        'title': r['title'],
        'upload_date': f"{year}-{month}-{day}",
        'user': r['uploader_id'],
        'view_count': r['view_count'],
        'like_count': r['like_count'],
        'dislike_count': r['dislike_count'],
        'thumbnail': r['thumbnail'],
        'width': r['width'],
        'height': r['height'],
        'categories': '|'.join(r['categories']) if r['categories'] is not None else None,
        'tags': '|'.join(r['tags']) if r['tags'] is not None else None,
        'channel_url': r['channel_url'],
        'description': r['description']
    }

    return video_info
