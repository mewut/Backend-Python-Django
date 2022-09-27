import logging
from django.core.mail import send_mail
from django.contrib.auth.models import User
from ...models import Post, Category
from datetime import timedelta
from django.utils import timezone


logger = logging.getLogger(__name__)


def my_job():
    now = timezone.now()
    list_week_posts = Post.objects.filter(dateCreation__gte=now - timedelta(days=7))

    for user in User.objects.filter():
        print('\nИмя пользователя:', user)
        print('e-mail пользователя:', user.email)
        # список групп-категорий, на которые подписан пользователь
        list_group_user = user.groups.values_list('name', flat=True)
        print('Состоит в группах:', list(list_group_user))
        #  список ID категорий из связанной модели Category по списку групп-категорий
        list_category_id = list(Category.objects.filter(name__in=list_group_user).values_list('id', flat=True))
        print('id категорий на которые подписан:', list_category_id)
        # отсеиваем посты, на которые пользователь не подписан
        list_week_posts_user = list_week_posts.filter(postCategory__in=list_category_id)
        print('Список постов, созданных за интересуемый период:\n', list(list_week_posts_user))
        if list_week_posts_user:
            # Подготовка сообщения для отправки письма
            list_posts = ''
            for post in list_week_posts_user:
                list_posts += f'\n{post}\nhttp://127.0.0.1:8000/news/{post.id}'

            send_mail(
                subject=f'News Portal: посты за прошедшую неделю.',
                message=f'Доброго дня, {user}!\nПредлагаем Вам ознакомиться с новыми постами, появившимися за последние 7 дней:\n{list_posts}',
                from_email='newsportal272@gmail.com',
                recipient_list=[user.email, ],
            )
