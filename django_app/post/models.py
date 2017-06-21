import re

# from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import reverse

'''
    member application생성
    User모델 구현,
        username, nickname
    이후 해당 User모델을 Post나 Comment에서 author나 user항목으로 참조
'''


# class User(models.Model):
#     name = models.CharField(max_length=30)


class Post(models.Model):
    # Django가 제공하는 기본 User와 연결되도록 수정
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    my_comment = models.OneToOneField(
        'Comment',
        blank=True,
        null=True,
        related_name='+',
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        through='PostLike'
    )

    class Meta:
        ordering = ['-pk']

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며
        # content를 content필드내용으로 넣는 Comment 객체 생성.
        return self.comment_set.create(
            author=user,
            content=content
        )

    @property
    def like_count(self):
        # 자신이 like하고 있는 user수 리턴
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'post_post_like_users'


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments',
    )

    def save(self, *args, **kwargs):
        # ex) 박보영 #여신 #존예 인스타
        # -> '박보영 <a href='#'>#여신</a> <a href='#'>#존예</a> 인스타
        # 해당내용을 self.html_content에 대입
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

    def make_html_content_and_add_tags(self, update=True):
        p = re.compile(r'(#\w+)')
        tag_name_list = re.findall(p, self.content)
        ori_content = self.content
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            change_tag = '<a href="{url}" class="hash-tag">{tag_name}</a>'.format(
                url=reverse('post:hashtag_post_list', kwargs={'tag_name': tag_name.replace('#', '')}),
                tag_name=tag_name
            )
            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        self.html_content = ori_content
        super().save(update_fields=['html_content'])
        # content에 포함된 Tag목록을 자신의


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)

        # 문서 4개
        # 쿠키 기반 사용자 요청 : http기반 요청은 매 연결이 연결되지 않는다. 계속 끊김 이걸 이용해서 쿠키기반 사용자 세션이라는 방식을 쓴다 세션에서 서버쪽에
        # 남겨놓엄 특정 키값을 클라이언트한테 부여 세션에서는 그 키값을 서버쪼에 저장하는 것을 세션이라고 한다 클라이언트 브라우저에서 키를 저장하는 것을 쿠킹이라고 한다

        # authentication : 사용자가 있는지 검증하는 것(인증)
        # authorization : 확인된 사용자가 권한이 있는지 확인 하는 것(권한 부여)
        # 플러그 가능한 백엔드 시스템 : 인증 백엔드 유저네임 페스워드 제공. 인증을 위해서 어떤 시스템을 제공함.
        # OAuth : 페이스북 구글의 것을 가져다 쓸 때 쓴다.
        # Django 인증 시스템 : 인증과 권한 부여

        # 장고에서 제공하는 User 사용하기
        # from django.contrib.auth.models import User 임포트해서 바로 사용하면 된다.

        # models.ImageField() 사용 할때 : 다음의 패키지를 설치해야 마이그레이션 할 수 있다.
        # pillow 파이썬에서 이미지처리를 할 때 여러가지 기능을 제공한다. image api
        # pil(파이썬 이미지 라이브러리)
        # 설치 방법
        # $ brew install libtiff libjpeg webp little-cms2
        # $ pip install Pillow
        # pip할 때는 가상환경 유의 !
        # crtl + shift + F

        # 유저모델을 한번 마이그레이션하면 바꾸기 힘들다 주의할 것(외래키와 다대다 관계를 가지기 때문. 바꾸면 일일이 수동으로 수정해야함)
