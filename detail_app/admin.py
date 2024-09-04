from django.contrib import admin
from .models import (Blog, BlogCategory, ContactUs, Favorite, Star)

admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(ContactUs)
admin.site.register(Favorite)
admin.site.register(Star)