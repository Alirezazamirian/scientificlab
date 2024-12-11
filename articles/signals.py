from django.db.models.signals import post_save
from django.dispatch import receiver
from detail_app.models import Star, LastArticle

@receiver(post_save, sender=Star)
def update_user_score(sender, instance, created, **kwargs):
    if created:
        article = instance.article
        total_score = Star.objects.filter(article=article)
        total_score_count = total_score.count()
        total_score_value = 0
        for item in total_score:
            total_score_value += item.score
        total_score_value = total_score_value / total_score_count
        LastArticle.objects.filter(id=article.id).update(score=total_score_value)
