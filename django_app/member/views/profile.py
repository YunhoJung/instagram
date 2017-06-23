from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from member.forms import UserEditForm

User = get_user_model()

__all__ = (
    'profile',
    'profile_edit',

)


def profile(request, user_pk=None):
    num_posts_per_page = 6
    # 0. urls.py와 연결
    # 1. user_pk에 해당하는 User를 cur_user키로 render
    # 2. member/profile.html작성, 해당 user정보 보여주기
    #   2-1. 해당 user의 followers, following목록 보여주기
    # 3. 현재 로그인한 유저가 해당 유저(cur_user)를 팔로우하고 있는지 여부 보여주기
    #   3-1. 팔로우하고 있다면 '팔로우 해제'버튼 아니라면 '팔로우'버튼 띄워주기.
    # 4~ -> def follow_toggle(request)뷰 생성

    # GET parameter에 들어온 'page'값 처리
    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user
    posts = user.post_set.order_by('-created_date')[:page * num_posts_per_page]
    post_count = user.post_set.count()
    next_page = page + 1 if post_count > page * num_posts_per_page else None
    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
    }
    return render(request, 'member/profile.html', context)





@login_required
def profile_edit(request):
    if request.method == "POST":
        # UserEditForm에 수정할 data를 함께 binding
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )
        # data가 올바를 경우 (유효성 통과)
        if form.is_valid():
            # form.save()를 이용해 instance를 update
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'member/profile_edit.html', context)


# url은 /member/signup/$
# member/signup.html을 사용
#   username, password1, password2를 받아 회원가입
#   이미 유저가 존재하는지 검사
#   password1, 2가 일치하는지 검사
#   각각의 경우를 검사해서 틀릴 경우 오류메시지 리턴
#   가입에 성공시 로그인시키고 post_list로 리다이렉트
