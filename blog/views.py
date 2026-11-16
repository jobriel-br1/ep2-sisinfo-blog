from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category
from .forms import PostForm

def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    User = get_user_model()
    users = User.objects.all()
    if request.method == 'POST':
        author_id = request.POST.get('author')
        text = request.POST.get('text')
        author = get_object_or_404(User, pk=author_id)
        Comment.objects.create(post=post, author=author, text=text)
        return redirect('post_detail', pk=post.pk)
    return render(request, 'comment_form.html', {'post': post, 'users': users})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.all().order_by('-post_date')
    return render(request, 'post_list.html', {'posts': posts, 'category': category})

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-post_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-post_date')
        return context
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

