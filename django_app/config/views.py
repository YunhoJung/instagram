from django.shortcuts import render, redirect

from post.models import Post


def index(request):
    return redirect('post:post_list')
