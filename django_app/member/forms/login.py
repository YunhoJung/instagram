from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     kwargs.setdefault('label_suffix', '')
    #     super().__init__(*args, **kwargs)  # 원래 이닛 다시 실행. 자신이 원래하던 과정을 거쳐가는데,

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': '사용자 아이디를 입력하세요',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )

    # is_valid를 실행했을 때, Form내부의 모든 field에 대한
    # 유효성 검증을 실행하는 메서드
    # 이미 존재하는 메서드 self.cleaned_data 리턴
    def clean(self):
        # clean()메서드를 실행한 기본결과 dict를 가져옴
        cleaned_data = super().clean()
        # username, password를 가져와 로컬변수에 할당
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # username, password를 이용해 사용자 authenticate
        user = authenticate(
            username=username,
            password=password,
        )
        # 인증에 성공할 경우, Form의 cleaned_data의 'user'
        # 키에 인증된 User객체를 할당
        if user is not None:
            self.cleaned_data['user'] = user
        # 인증에 실패한 경우,
        else:
            raise forms.ValidationError(
                'Login credentials not valid'
            )
        return self.cleaned_data

        # 장고에서 form이 어떻게 동작하는지
        # request는 폼말고 뷰에서 !
        # 유효성 검사를 왜하는지? 클린 메서드의 의미.
        # def __init__ 부분은 form 에서 : 없애기 위해 / label_suffix가 None이 아니라 값이 주어지면
        # 이것을 이용해 form을 만든다. kwargs는 같은 변수를 가리킴.
        # 위치인자, 키워드인자, 키워드인자는 딕셔러니 형태
        # setdefault메서드는 set역할. 'label_suffix'라는 값이 없으면 만들고서 ''값을 넣어준다.
        # super() 상속받은 부분, 즉 나머지는 알아서 해라 ! 부모꺼를 오버라이드하면서도 부모의 동작을 할 때.
        # widget이란 ?? input 타입을 설정하는 것과 유사. 어떤 속성이 나올 것인가를 결정.
        # form field가 따로 있음 model field와 유사하지만 다름
        # widget은 Textinput이 기본
        # 바운드 폼은 뒤에 딕셔너리 형태의 데이터를 가지는데 굳이 설정해줄 필요는 없다
        # request.POST가 이미 딕셔너리 형태로 데이터를 가지기 때문이다
        # Form을 이용해 데이터 검증
        # 유저네임 벨리데이터 패스워드 벨리데이터 장고에 내장되어 있는 벨리데이터(정규표현식으로 되어있음)

        # 유효성을 통과하면 파이썬 객체를 생성해야한다?
        # form은 스트링으로 받는데 플로트를 받고싶으면 floatfield 사용
        # clean_<fieldname>은 특정필드를 하나씩 유효성 검사할 때 사용 -> 폼 차원에서 클린
        # 필드 자체에서 유효성검사는 Field.clean()
        # Form.clean()
        # super().clean()을 쓰거나(리턴값이 있다고 가정할때 혹은 그런 상황일때) self.cleaned_data(super에서 가져올 값이 없을 때)

        #