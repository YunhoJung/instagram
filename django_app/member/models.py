import re

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.db import models

from utils.fields.custom_imagefield import CustomImageField


class UserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id']
        )
        user, user_created = self.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'last_name': user_info.get('last_name', ''),
                'first_name': user_info.get('first_name', ''),
                'email': user_info.get('email', ''),
            }
        )
        #
        if user_created:
            url_picture = user_info['picture']['data']['url']
            p = re.compile(r'.*\.([^?]+)')
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                user.pk,
                file_ext,
            )
            temp_file = NamedTemporaryFile(delete=False)
            response = requests.get(url_picture)
            temp_file.write(response.content)
            user.img_profile.save(file_name, File(temp_file))
            # User.objects.create_user
        return user


class User(AbstractUser):
    # 이 User모델을 AUTH_USER_MODEL로 사용하도록 settings.py에 설정
    '''
    동작
    follow : 내가 다른 사람을 follow 함
    unfollow : 내가 다른 사람에게 한 follow를 취소함

    속성
    followers : 나를 follow하고 있는 사람들
    follower : 나를 followㅏ고 있는 사람
    following : 내가 follow하고 있는 사람들
    friend : 나와 서로 follow하고 있는 관계
    friedns : 나와 서로 follow하고 있는 모든 관계

    ex) 내가 박보영을 follow하고 고성현과 김수정은 나를 follow한다
        나의 followers는 고성현 김수정
        나의 following은 박보영
        김수정은 나의 follower이다
        나는 박보영의 follower이다.
        나와 고성현은 friedn관계이다.
        나의 friends

    '''
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)
    nickname = models.CharField(max_length=24, null=True, unique=True)
    img_profile = CustomImageField(
        upload_to='member-%y%m%d',
        blank=True,
        # default_static_image='images/profile.png',
    )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username

    def follow(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')
        self.following_relations.get_or_create(
            to_user=user,
        )

    def unfollow(self, user):
        Relation.objects.filter(
            from_user=self,
            to_user=user,
        ).delete()

    def is_follow(self, user):
        return self.following.relations.filter(to_user=user).exists()

    def is_follower(self, user):
        return self.follower.relations.filter(from_user=user).exists()

    # 해당 user를 내가 follow하고 있는지 bool여부를 반환

    def follow_toggle(self, user):
        # 이미 follow상태면 unfollow로 아닐경우 follow상태로 만듬
        relation, relation_created = self.followering_relations.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

    @property
    def following(self):
        relations = self.following_relations.all()
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.follower_relations.all()
        return User.objects.filter(pk__in=relations.values('from_user'))


class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='following_relations')
    to_user = models.ForeignKey(User, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from({}) to ({})'.format(
            self.from_user,
            self.to_user,
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )


        # member.admin / 페이지 오류 / migrations


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
