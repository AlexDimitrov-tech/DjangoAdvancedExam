from django.views.generic import TemplateView

from catalog.models import Category, Game


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_count'] = Game.objects.count()
        context['category_count'] = Category.objects.count()
        context['latest_games'] = Game.objects.select_related('owner').prefetch_related('categories')[:3]
        return context
