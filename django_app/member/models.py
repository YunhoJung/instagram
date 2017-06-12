from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 이 User모델을 AUTH_USER_MODEL로 사용하도록 settings.py에 설정
    pass


# abstract User 사용하기
# ./manage.py startapp member
# settings.py 설정
# AUTH_USER_MODEL = member.User
# from django.conf import settings하고
# 기존에 User 클래스를 settings.AUTH_USER.MODEL로 대체
# 이런 식으로 CustomUser를 사용할 수 있다.
# 만약 중간에 유저모델을 바꾸는 경우라면 데이터베이스를 전부 다 지우고 처음부터 새로 migrations migrate해주면 된다.