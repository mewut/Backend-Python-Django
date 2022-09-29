from celery import shared_task
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
import time

from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


@shared_task
def add_post_send_email(category, id):   # или post вместо id...
    # подписчикам о новых постах
    try:
        post = Post.objects.get(id=id)
        category_group = Group.objects.get(name=category)
        list_mail = list(User.objects.filter(groups=category_group).values_list('email', flat=True))
        for user_email in list_mail:
            username = list(User.objects.filter(email=user_email).values_list('username', flat=True))[0]
            html_content = render_to_string('subscribe_new_post.html', {'post': post, 'username': username, 'category': category})
            msg = EmailMultiAlternatives(
                subject=f'NewsPortal: {category}',
                body='',
                from_email='transmet97@gmail.com',
                to=[user_email, ],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Group.DoesNotExist:
        pass

@shared_task
def send_mail_monday_8am():
    # рассылка в 8 утра
    now = timezone.now()
    list_week_posts = Post.objects.filter(dateCreation__gte=now - timedelta(days=7))

    for user in User.objects.filter():
        print('\nИмя пользователя:', user)
        print('email пользователя:', user.email)
        list_group_user = user.groups.values_list('name', flat=True)
        print('Состоит в группах:', list(list_group_user))
        list_category_id = list(Category.objects.filter(name__in=list_group_user).values_list('id', flat=True))
        print('id категорий на которые подписан:', list_category_id)
        list_week_posts_user = list_week_posts.filter(postCategory__in=list_category_id)
        print('Список постов, опубликованных за неделю:\n', list(list_week_posts_user))
        if list_week_posts_user:
            list_posts = ''
            for post in list_week_posts_user:
                list_posts += f'\n{post}\nhttp://127.0.0.1:8000/news/{post.id}'

            send_mail(
                subject=f'NewsPortal: посты за прошедшую неделю.',
                message=f'Доброго дня, {user}!\nНовости за последние 7 дней:\n{list_posts}',
                from_email='transmet97@gmail.com',
                recipient_list=[user.email, ],
            )


def hello():
    return None
