from django.contrib import admin
from .models import (HeadArticle, SubHeadArticle, MiddleArticle, LastArticle)

admin.site.register(HeadArticle)
admin.site.register(SubHeadArticle)
admin.site.register(MiddleArticle)
admin.site.register(LastArticle)
