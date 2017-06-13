from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    # /post/3/$, /post/35/$
    # 정규표현식에서 매칭된 그룹을 위치인수로 변환하는 방법
    # url(r'(^\d+)/$', views.post_detail),

    # 정규표현식에서 매칭된 그룹을 키워드인수로 변환하는 방법
    # 그룹의 가장 앞부분에 ?P<패턴이름>을 지정
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
]

# \d+ -> 숫자 한개 이상
