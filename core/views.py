from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    post_list = Post.objects.all()
    return render(request, "index.html", {"post_list": post_list})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "post_detail.html", {"post": post})
