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


# create_user라는 메서드를 통해 유저 생성 is_staff is_superuser set_password authenticate() 메서드 == 은 값을 비교 하는 것.
# is, is not은 객체를 비교하는 것. singleton(None처럼 객체 하나를 설정해놓고 가져다 쓰는 객체)의 경우 is로 비교하는게 빠름.
# 