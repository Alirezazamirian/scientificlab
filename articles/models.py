from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from utils.models import GeneralDateModel
from django.utils.translation import gettext as _

ISFREE_ARTICLE = (
    ('Test', 'تست'),
    ('Experiment', 'آزمایش'),
)


class HeadArticle(GeneralDateModel):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True, max_length=500)

    class Meta:
        verbose_name = _('Head Article')
        verbose_name_plural = _('Head Articles')

    def __str__(self):
        return self.title


class SubHeadArticle(GeneralDateModel):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True, max_length=500)
    is_free = models.BooleanField(default=False, verbose_name=_('Is Free'))
    type = models.CharField(max_length=50, verbose_name=_('Type'), choices=ISFREE_ARTICLE)
    head_article = models.ForeignKey(HeadArticle, on_delete=models.CASCADE, verbose_name=_('Head Article'))

    class Meta:
        verbose_name = _('Sub Head Article')
        verbose_name_plural = _('Sub Head Articles')

    def __str__(self):
        return self.title


class MiddleArticle(GeneralDateModel):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True, max_length=500)
    sub_head_article = models.ForeignKey(SubHeadArticle, on_delete=models.CASCADE, verbose_name=_('Sub Head Article'),
                                         blank=True, null=True)

    class Meta:
        verbose_name = _('Middle Article')
        verbose_name_plural = _('Middle Articles')

    def __str__(self):
        return self.title


class LastArticle(GeneralDateModel):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'), max_length=500)
    image = models.ImageField(verbose_name=_('Image'), upload_to=f'article/{title}', null=True, blank=True)
    sub_head_article = models.ForeignKey(SubHeadArticle, on_delete=models.CASCADE, verbose_name=_('Sub Head Article'),
                                         blank=True, null=True)
    middle_article = models.ForeignKey(MiddleArticle, on_delete=models.CASCADE, verbose_name=_('Middle Article'),
                                       blank=True, null=True)
    abbreviation_name = models.CharField(max_length=50, verbose_name=_('Abbreviation'), null=True, blank=True)
    score = models.IntegerField(verbose_name=_('Score'), default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = _('Last Article')
        verbose_name_plural = _('Last Articles')

    def __str__(self):
        return self.title
