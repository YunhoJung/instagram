from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 HTML
    # POST요청이 올 경우 좌측 코드를 기반으로 로그인 완료 후 post_list로 이동
    # 실해할 경우 HttpResponse로 'Login invalid!' 띄어주기

    # member/urls.py 생성
    # /member/login/으로 접근시 이 view로 오도록 설정
    # config/urls.py에 member/urls.py를 include
    #   member/urls.py에 app_name설정으로 namespace지정
    if request.method == 'POST':
        # username = request.Post('username')
        # password = request.Post('password')
        # user = authenticate(request, username=username,)
        # return HttpResponseRedirect(request, 'post:post_list')
    else:
        return render(request, 'member/login.html')
