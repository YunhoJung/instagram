from django.db import models
from django.contrib.auth.models import User

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
    author = models.ForeignKey(User)
    photo = models.ImageField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        User,
        related_name='like_posts',
        through='PostLike'
    )
    tags = models.ManyToManyField('Tag')

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며
        # content를 content필드내용으로 넣는 Comment 객체 생성.
        return self.comment_set.create(
            author=user,
            content=content
        )

    def add_tag(self, tag_name):
        # tags에 tag매개변수로 전달된 값(str)을
        # name으로 갖는 Tag객체를 (이미 존재하면) 가져오고 없으면 생성하여
        # 자신의 tag에 추가
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if not self.tags.filter(name=tag_name).exists():
            self.tags.add(tag)


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'post_post_like_users'


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        User,
        through='CommentLike',
        related_name='like_comments',
    )


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
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
