from django.forms import DateInput
import django.forms
import django_filters
from django.db import models
from django_filters import FilterSet, ModelMultipleChoiceFilter, ModelChoiceFilter, NumberFilter, DateFilter
from .models import Post, Category, Author


class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='category__cat_thru',
        queryset=Category.objects.all(),
        label='Category',
        conjoined=True,
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Any',
    )

    time_pub = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    # time_pub = NumberFilter(field_name='time_pub', lookup_expr='date_pub')
    # time_pub__gt = NumberFilter(field_name='time_pub', lookup_expr='date_pub__gt')

    class Meta:
        model = Post
        fields = {
            # поиск по названию
            'title': ['icontains'],
            'author': ['exact'],
            'rating': [
                'lt',  # рейтинг меньше или равен указанному
                'gt',  # рейтинг больше или равен указанному
            ],
            # 'time_pub': ['gte'],
        }
        filter_overrides = {
            models.DateTimeField: {
                'filter_class' : django_filters.DateFilter,
                'extra' : lambda f: {
                    'lookup_expr' : 'gte',
                },
            },
        }
