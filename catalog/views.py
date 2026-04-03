from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import GameForm
from .models import Game


class GameListView(ListView):
	model = Game
	template_name = 'catalog/game_list.html'
	context_object_name = 'games'


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
