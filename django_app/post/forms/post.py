from django import forms

from ..models import Post


class PostForm(forms.ModelForm):
    # 생성자를 조작해서 실제 Post의 photo필드는 blank=True
    # (Form에서 required=False)이지만,
    # Form을 사용할 때는 반드시 photo를 받도록 함
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True

    comment = forms.CharField(
        required=False,
        widget=forms.TextInput
    )

    class Meta:
        model = Post
        fields = (
            'photo',
            'comment',
        )

    def save(self, **kwargs):
        # 전달된 키워드 인수 중 'commit'키 값을 가져옴
        commit = kwargs.get('commit', True)
        # 전달된 키워드 인수 중 'author'키 값을 가져오고, 기존  kwargs dict에서 제외
        author = kwargs.pop('author', None)

        # super()의 save()호출
        self.instance.author = author
        instance = super().save(**kwargs)

        comment_string = self.cleaned_data['comment']
        if commit and comment_string:
            instance.comment_set.create(
                author=instance.author,
                content=comment_string,
            )
        return instance

# context_processors 만든 이유?
