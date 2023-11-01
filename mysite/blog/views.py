from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, CreateView
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        tag = self.request.GET.get('tag','')
        if q:
            qs = qs.filter(title__icontains=q)
        elif tag:
            qs = qs.filter(tags__name=tag)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):   # pk를 받으려면 여기 form처럼 추가해서 적용 가능
        video = form.save(commit=False)
        video.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def get_object(self, queryset=None):
        '''
        PostDetailView.as_view()에서 사용할 object를 반환하는 함수
        여기서 원하는 쿼리셋이나 object를 추가한 후 템플릿으로 전달 가능
        수정한 후 전달도 가능
        '''
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)


#UserPassesTestMixin를 쓰면 test_func으로 테스트 가능 (유닛 테스트 그런게 아니라 여기 접근할 수 있는 자격을 test하는 느낌?)
class PostUpdateView(UserPassesTestMixin, UpdateView):  
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/blog_form.html'

    def test_func(self): #UserPassesTestMixin에 있고 test_func() 메서드를 오버라이딩. True, False값으로 접근 제한 가능
        return self.get_object().author == self.request.user


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    
    def test_func(self): #UserPassesTestMixin에 있고 test_func() 메서드를 오버라이딩. True, False값으로 접근 제한 가능
        return self.get_object().author == self.request.user


post_list = PostListView.as_view()
post_new = PostCreateView.as_view()
post_detail = PostDetailView.as_view()
post_edit = PostUpdateView.as_view()
post_delete = PostDeleteView.as_view()

@login_required
def comment_new(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # commit=False는 DB에 저장하지 않고 객체만 반환
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('tube:post_detail', pk)
    else:
        form = CommentForm()
    return render(request, 'tube/form.html', {
        'form': form,
    })

@login_required
def comment_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # commit=False는 DB에 저장하지 않고 객체만 반환
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('tube:post_detail', pk)
    else:
        form = CommentForm()
    return render(request, 'tube/form.html', {
        'form': form,
    })