from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from datetime import datetime
from .models import Post, Author
from .forms import PostForm, ProfileUserForm


def index(request):
    return render(request, 'news/news.html')


def news_home(request):
    news = Post.objects.all()
    return render(request, 'news.html', {'news' : news})


class News(ListView):
    model = Post
    ordering = '-dateCreation', 'rating'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class SearchList(ListView):
    model = Post
    ordering = '-dateCreation', 'rating'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get.queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('product_list')


class PostCreateArticle(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdateArticle(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ProfileUserUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    model = Author
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('home')

