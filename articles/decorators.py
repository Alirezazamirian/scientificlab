from django.http import JsonResponse
from functools import wraps
from .models import LastArticle, MiddleArticle


def payment_required(instance=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            condition = instance(request) if instance else None
            if request.user.is_authenticated:
                if isinstance(condition, LastArticle) and (condition.sub_head_article.is_free or condition.middle_article.sub_head_article.is_free):
                    pass
                elif isinstance(condition, LastArticle) and (not condition.sub_head_article.is_free or not condition.middle_article.sub_head_article.is_free):
                    if not request.user.is_pay:
                        return JsonResponse(
                            {'error': 'Access denied. Payment required to access this resource.'},
                            status=403
                        )
                elif isinstance(condition, MiddleArticle) and condition.sub_head_article.is_free:
                    pass
                elif isinstance(condition, MiddleArticle) and not condition.sub_head_article.is_free:
                    if not request.user.is_pay:
                        return JsonResponse(
                            {'error': 'Access denied. Payment required to access this resource.'},
                            status=403
                        )
            else:
                return JsonResponse(
                    {'error': 'Authentication required.'},
                    status=401
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
