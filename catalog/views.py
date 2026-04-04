from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import GameForm
from .models import Game


class GameListView(ListView):
	model = Game
	template_name = 'catalog/game_list.html'
	context_object_name = 'games'
	paginate_by = 8

	def get_queryset(self):
		query = self.request.GET.get('q', '').strip()
		queryset = (
			Game.objects.select_related('owner')
			.prefetch_related('categories')
		)
		if query:
			queryset = queryset.filter(
				Q(title__icontains=query)
				| Q(description__icontains=query)
				| Q(categories__name__icontains=query)
				| Q(owner__username__icontains=query)
			).distinct()
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = self.request.GET.get('q', '').strip()
		return context


class GameDetailView(DetailView):
	model = Game
	template_name = 'catalog/game_detail.html'
	context_object_name = 'game'


class GameCreateView(LoginRequiredMixin, CreateView):
	model = Game
	form_class = GameForm
	template_name = 'catalog/game_form.html'

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('catalog:game-detail', kwargs={'pk': self.object.pk})
