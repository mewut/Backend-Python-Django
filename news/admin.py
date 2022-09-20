from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
# admin.site.register(Product)
admin.site.register(Author)