from django import template

register = template.Library()


@register.filter
def stars(value: int) -> str:
    try:
        rating = int(value)
    except (TypeError, ValueError):
        return ''
    rating = max(0, min(5, rating))
    return '★' * rating + '☆' * (5 - rating)
