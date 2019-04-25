from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    """
    处理表单请求
    :param request:
    :param post_pk:
    :return:
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 检查数据是否合法,调用表单的save()方法,保存到数据库
            comment = form.save(commit=False)
            comment.post = post
            # 将评论保存进数据库
            comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。

            return redirect(post)

        else:
            # 其他情况的处理方式
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog\detail.html', context=context)
        # 不是post请求,说明没有
    return redirect(post)
