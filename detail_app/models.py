from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from utils.models import GeneralDateModel
from articles.models import LastArticle
from accounts.models import User
from django.utils.translation import gettext as _



class ContactUs(GeneralDateModel):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), max_length=500)
    answer = models.TextField(verbose_name=_('Answer'), null=True, blank=True)
    is_answered = models.BooleanField(verbose_name=_('Is Answered'), default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    type = models.CharField(verbose_name=_('Type'), max_length=40)

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')

    def __str__(self):
        return f'{self.title} - {self.user.full_name}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    articles = models.ForeignKey(LastArticle, verbose_name=_('Articles'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')

    def __str__(self):
        return f'{self.user.full_name} - {self.articles.title}'


class Blog(GeneralDateModel):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), max_length=2000)
    image = models.ImageField(verbose_name=_('Image'), upload_to='blog', null=True, blank=True)
    category = models.ForeignKey('BlogCategory', on_delete=models.CASCADE, verbose_name=_('Category'), null=True, blank=True)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def __str__(self):
        return f'{self.title} - {self.description[:20]}'


class BlogCategory(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')

    def __str__(self):
        return f'{self.title}'


class Star(models.Model):
    score = models.IntegerField(verbose_name=_('Score'), default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name=_('User'))
    article = models.ForeignKey(LastArticle, on_delete=models.CASCADE, verbose_name=_('Article'))

    class Meta:
        verbose_name = _('Star')
        verbose_name_plural = _('Stars')

    def __str__(self):
        return f'{str(self.score)} - {self.user.full_name}'


class TicketCategory(models.Model):
    type = models.CharField(verbose_name=_('Type'), max_length=40)

    class Meta:
        verbose_name = _('Ticket Category')
        verbose_name_plural = _('Ticket Categories')

    def __str__(self):
        return f'{self.type}'


class Ticket(GeneralDateModel):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), max_length=500)
    is_answered = models.BooleanField(verbose_name=_('Is Answer'), default=False)
    ticket_category = models.ForeignKey('TicketCategory', on_delete=models.CASCADE, verbose_name=_('Ticket Category'))

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return f'{self.title}'

class TicketConversation(GeneralDateModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Ticket Conversation')
        verbose_name_plural = _('Ticket Conversations')

    def __str__(self):
        return f'{self.ticket.ticket_category.type} --- {self.user.phone} --- {self.user.email}'

