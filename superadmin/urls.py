from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('payment/', views.UserPayment.as_view(), name='UserPayment'),
    path('payment-date/', views.UserPaymentDate.as_view(), name='UserPaymentDate'),
    path('user-branch/', views.UserBranchCount.as_view(), name='UserBranchCount'),
    path('user-donation-count/', views.UserDonations.as_view(), name='UserDonations'),
]

router = routers.DefaultRouter()
router.register(r'users-admin', views.ManageUsers)
urlpatterns += router.urls

contactus_router = routers.DefaultRouter()
contactus_router.register(r'contact-us-admin', views.ManageContactUs)
urlpatterns += contactus_router.urls

article_router = routers.DefaultRouter()
article_router.register(r'articles-admin', views.ManageAllArticles)
urlpatterns += article_router.urls

blogcat_router = routers.DefaultRouter()
blogcat_router.register(r'blog-category-admin', views.ManageCategoryBlog)
urlpatterns += blogcat_router.urls

blog_router = routers.DefaultRouter()
blog_router.register(r'blog-admin', views.ManageBlog)
urlpatterns += blog_router.urls

sub_article = routers.DefaultRouter()
sub_article.register(r'sub-article-admin', views.ManageSubArticles)
urlpatterns += sub_article.urls

middle_article = routers.DefaultRouter()
middle_article.register(r'middle-article-admin', views.ManageMiddleArticles)
urlpatterns += middle_article.urls

head_article = routers.DefaultRouter()
head_article.register(r'head-article-admin', views.ManageHeadArticles)
urlpatterns += head_article.urls

last_article = routers.DefaultRouter()
last_article.register(r'last-article-admin', views.ManageLastArticles)
urlpatterns += last_article.urls

article_desc = routers.DefaultRouter()
article_desc.register(r'desc-article-admin', views.ManageDescriptionArticles)
urlpatterns += article_desc.urls

article_image = routers.DefaultRouter()
article_image.register(r'image-article-admin', views.ManageImageArticles)
urlpatterns += article_image.urls

admin_ticket = routers.DefaultRouter()
admin_ticket.register(r'ticket-response-admin', views.ManageAdminTickets)
urlpatterns += admin_ticket.urls

ticket_router = routers.DefaultRouter()
ticket_router.register(r'tickets-list-get-admin', views.ManageTickets)
urlpatterns += ticket_router.urls

ticket_cat_router = routers.DefaultRouter()
ticket_cat_router.register(r'tickets-category-admin', views.ManageTicketsCategory)
urlpatterns += ticket_cat_router.urls
