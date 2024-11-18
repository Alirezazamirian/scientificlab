from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('payment/', views.UserPayment.as_view(), name='UserPayment'),
]

router = routers.DefaultRouter()
router.register(r'users', views.ManageUsers)
urlpatterns += router.urls

article_router = routers.DefaultRouter()
article_router.register(r'articles', views.ManageArticles)
urlpatterns += article_router.urls

ticket_router = routers.DefaultRouter()
ticket_router.register(r'tickets', views.ManageTickets)
urlpatterns += ticket_router.urls

contactus_router = routers.DefaultRouter()
contactus_router.register(r'contact-us', views.ManageContactUs)
urlpatterns += contactus_router.urls

blogcat_router = routers.DefaultRouter()
blogcat_router.register(r'blog-category', views.ManageCategoryBlog)
urlpatterns += blogcat_router.urls

blog_router = routers.DefaultRouter()
blog_router.register(r'contact-us', views.ManageBlog)
urlpatterns += blog_router.urls
