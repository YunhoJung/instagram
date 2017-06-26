import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.shortcuts import render, redirect

from ..forms import LoginForm, SignupForm

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login'
)


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
        # 요청받은 POST데이터에서 username, password키가 가진 값들을
        # username, password변수에 할당 (문자열)
        # username = request.POST['username']
        # password = request.POST['password']
        # authenticate함수를 사용해서 User객체를 얻어 user에 할당
        # 인증에 실패할 경우 user변수에는 None이 할당됨
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password,
        # )
        # if user is not None:
        # # Django의 session을 이용해 이번 request와 user객체를 사용해 로그인 처리
        #     # 이후의 request/response에서는 사용자가 인증된 상태로 통신이 이루어진다
        #     django_login(request, user)
        #     # 로그인 완료 후에는 post_list뷰로 리다이렉트 처리
        #     return redirect('post:post_list')
        # # user변수가 None일 경우 (username 또는 password가 틀려 인증에 실패한 경우)

        # Form 클래스 사용시
        # Bound form 생성
        form = LoginForm(data=request.POST)
        # Bound form의 유효성을 검증 통과하면 true bool 반환
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            # 일반적인 경우에는 post_list로 이동하지만,
            # GET parameter의 next속성값이 있을 경우 해당 URL로 이동
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_list')


            # user변수가 None이 아닐 경우 (정상적으로 인증되어 User객체를 얻은 경우)
            #
    # get 요청이 왔을 경우, 단순 로그인 Form 보여주기
    else:
        # 만약 이미 로그인 된 상태일 경우에는
        # post_list로 redirect
        # 아닐경우 login.html을 render해서 리턴
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()  # unbound form
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context=context)


    # render, redirect, httpresponse, ??


def logout(request):
    # 로그아웃되면 post_list로 redirect
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == "POST":
        #     username = request.POST['username']
        #     password1 = request.POST['password1']
        #     password2 = request.POST['password2']
        #     if User.objects.filter(username=username).exists():
        #         return HttpResponse('Username is already exist')
        #     elif password1 != password2:
        #         return HttpResponse('Password and Password check are not equal')
        #     user = User.objects.create_user(
        #         username=username,
        #         password=password1
        #     )
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.create_user()
            # if User.objects.filter(username=username).exists():
            #         return HttpResponse('Username is already exist')
            #     elif password1 != password2:
            #         return HttpResponse('Password and Password check are not equal')
            #     user = User.objects.create_user(
            #         username=username,
            #         password=password1
            #     )
            #
            django_login(request, user)
            return redirect('post:post_list')

    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)


def facebook_login(request):
    code = request.GET.get('code')
    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
    )

    class GetAccessTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['data']['error']
            self.code = error_dict['code']
            self.message = error_dict['message']
            self.is_valid = error_dict['is_valid']
            self.scopes = error_dict['scopes']

    class DebugTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['data']['error']
            self.code = error_dict['code']
            self.message = error_dict['message']

    def add_message_and_redirect_referer():
        error_message_for_user = 'Facebook login error'
        messages.error(request, error_message_for_user)
        return redirect(request.META['HTTP_REFERER'])

    def get_access_token(code):
        url_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'
        redirect_uri = '{}://{}{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
        )
        # facebook_login view가 처음 호출될 때 'code' reqeust GET parameter

        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        print(url_access_token_params)
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()
        if 'access_token' in result:
            return result['access_token']
        elif 'error' in result:
            raise GetAccessTokenException(result)
            # error_message = 'Facebook login error\n type: {}\n message: {}'.format(
            #     result['error']['type'],
            #     result['error']['message'],
            #
            # )
            # print(error_message)
            # messages.error(request, error_message)
            # return redirect(request.META['HTTP_REFERER'])
        else:
            raise Exception('Unknown error')

    def debug_token(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        if 'error' in result['data']:
            raise DebugTokenException(result['data']['error'])
        else:
            return result

    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/{user_id}'.format(user_id=user_id)
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'first_name',
                'last_name',
                'picture.type(large)',
                'gender',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result

    if not code:
        return add_message_and_redirect_referer()
    try:
        access_token = get_access_token(code)
        debug_result = debug_token(access_token)
        user_info = get_user_info(user_id=debug_result['data']['user_id'], token=access_token)
        user = User.objects.get_or_create_facebook_user(user_info)

        django_login(request, user)
        return redirect(request.META['HTTP_REFERER'])
    except GetAccessTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
