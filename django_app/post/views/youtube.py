import requests
from django.shortcuts import render

__all__ = (
    'youtube_search',
)


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
        # videos = Video.objects.filter(Q(title__contains=q) | Q(description__contains=q))
        context = {
            'response': response.json(),
        }
    else:
        context = {}
    return render(request, 'post/youtube_search.html', context)
