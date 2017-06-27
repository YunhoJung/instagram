import re
from pprint import pprint

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q
from django.shortcuts import render

from ..models import Video

__all__ = (
    'youtube_search',
    'youtube_create',
)


# [1] 검색결과를 DB에 저장하고, 해당내용을 템플릿에서 보여주기!
# 1. 유튜브 영상을 저장할 class Video(models.Model)생성
# 2. 검색결과의 videoId를 Video의 youtube_id필드에 저장
#       해당필드는 unique해야 함
# 3. 검색결과에서 videoId가 Video의 youtube_id와 일치하는 영상이 이미 있을경우에는 pass,
#    없을경우 새 Video객체를 만들어 DB에 저장
# 4. 이후 검색결과가 아닌 자체 DB에서 QuerySet을 만들어 필터링한 결과를 템플릿에서 표시


def youtube_create(request):
    video_db_set = Video.objects.all()
    video_id_set = [i.video_id for i in video_db_set]
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')
    print(q)
    if q:
        search_param = {
            'part': 'snippet',
            'key': 'AIzaSyB8sTxOqHZpItlVlJKP0ETvO0f8ZsiR70Q',
            'q': q,
            'maxResults': 10,
            'type': 'video',
        }
        response = requests.get(url_api_search, params=search_param)
        # videos = Video.objects.filter(Q(title__contains=q) | Q(description__contains=q))
        result = response.json()

        for item in result['items']:
            if item['id']['videoId'] in video_id_set:
                break
            else:
                url_thumbnails = item['snippet']['thumbnails']['high']['url']
                p = re.compile(r'.*\.([^?]+)')
                file_ext = re.search(p, url_thumbnails).group(1)
                file_name = '{}.{}'.format(
                    item['id']['videoId'],
                    file_ext,
                )
                temp_file = NamedTemporaryFile()
                response = requests.get(url_thumbnails)
                temp_file.write(response.content)

                video = Video.objects.create(
                    video_id=item['id']['videoId'],
                    title=item['snippet']['title'],
                    video_description=item['snippet']['description'],
                    created_date=item['snippet']['publishedAt'],
                )
                video.thumbnail.save(file_name, File(temp_file))

        videos = Video.objects.filter(Q(title__contains=q) | Q(video_description__contains=q))
        context = {
            'response': response.json(),
            'videos': videos,
        }
        pprint(response.json())
    return render(request, 'post/youtube_search.html', context)


def youtube_search(request, q=None):
    # search list API를 이용해서 (type: video, maxResults: 10)
    # request.GET.get('q')에 데이터가 있을 경우
    # request.get을 사용한 결과를 변수에 할당하고
    # 해당 변수를 템플릿에서 표시
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')
    print(q)
    if q:
        search_param = {
            'part': 'snippet',
            'key': 'AIzaSyB8sTxOqHZpItlVlJKP0ETvO0f8ZsiR70Q',
            'q': q,
            'maxResults': 10,
            'type': 'video',
        }
        response = requests.get(url_api_search, params=search_param)

        context = {
            'response': response.json(),
        }
    else:
        context = {}
    return render(request, 'post/youtube_search.html', context)
