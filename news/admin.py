from django.contrib import admin
from .models import Author, Category, Post, CategoryPost, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(CategoryPost)
admin.site.register(Comment)
