from django.contrib import admin
from .models import (Blog, BlogCategory, ContactUs, Favorite, Star, Ticket, TicketCategory, TicketConversation)

admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(ContactUs)
admin.site.register(Favorite)
admin.site.register(Star)
admin.site.register(TicketCategory)
admin.site.register(Ticket)
admin.site.register(TicketConversation)
