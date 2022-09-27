from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .models import Post, Author, Category, PostCategory
from .forms import PostForm, ProfileUserForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
from django.apps import AppConfig


class News(ListView):
    model = Post
    ordering = '-dateCreation', 'rating'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_in_page'] = self.paginate_by
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post_search'
    ordering = ['-dateCreation']
    filter_class = PostFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=queryset)
        return self.filter.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        context['list_in_page'] = self.paginate_by  # количество выведенных публикаций на странице
        context['all_posts'] = Post.objects.all()  # общее количество публикаций на сайте
        return context


# addpost = Signal(providing_args=['instance', 'category'])


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save()
        id = post.id
        a = form.cleaned_data['postCategory']
        category_object_name = a[0]
        addpost.send(Post, instance=post, category=category_object_name)
        return redirect(f'/news/{id}')


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def add_subscribe(request, pk):     # pk = id новости
    user = request.user
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    add_subscribe = Category.objects.get(name=category_object_name)
    add_subscribe.subscribers = user
    add_subscribe.save()
    # user.category_set.add(add_subscribe)

    send_mail(
        subject=f'News Portal: {category_object_name}',
        message=f'Доброго дня, {request.user}! Вы подписались на уведомления о выходе новых статей в категории {category_object_name}',
        from_email='newsportal272@gmail.com',
        recipient_list=[user.email, ],
    )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def del_subscribe(request, pk):
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    del_subscribe = Category.objects.get(name=category_object_name)
    del_subscribe.subscribers = None
    del_subscribe.save()
    user = request.user

    send_mail(
        subject=f'News Portal: {category_object_name}',
        message=f'Доброго дня, {request.user}! Вы отменили уведомления о выходе новых статей в категории {category_object_name}. Нам очень жаль, что данная категория Вам не понравилась, ждем Вас снова на нашем портале!',
        from_email='newsportal272@gmail.com',
        recipient_list=[user.email, ],
    )
    return redirect(request.META.get('HTTP_REFERER'))


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
