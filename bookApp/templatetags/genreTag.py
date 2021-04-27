from django import template
from django.db.models import Count

from ..models import Genre

register = template.Library()


@register.inclusion_tag('BookApp/genreList.html')
def show_genres():
    genres = Genre.objects.all()
    context = {
        "genres": genres,
    }
    return context
