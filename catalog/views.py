from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from boardgameconnect.mixins import OwnerOrStaffRequiredMixin
from rentals.models import RentalRequest
from reviews.models import Review

from .forms import CategoryDeleteForm, CategoryForm, GameDeleteForm, GameForm
from .models import Category, Game


class CategoryListView(ListView):
	model = Category
	template_name = 'catalog/category_list.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return Category.objects.select_related('created_by').prefetch_related('games')


class CategoryDetailView(DetailView):
	model = Category
	template_name = 'catalog/category_detail.html'
	context_object_name = 'category'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['games'] = self.object.games.select_related('owner')
		return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	form_class = CategoryForm
	template_name = 'catalog/category_form.html'

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		messages.success(self.request, 'Category created successfully.')
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('catalog:category-detail', kwargs={'pk': self.object.pk})


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	form_class = CategoryForm
	template_name = 'catalog/category_form.html'

	def dispatch(self, request, *args, **kwargs):
		category = self.get_object()
		if category.can_user_manage(request.user):
			return super().dispatch(request, *args, **kwargs)
		raise PermissionDenied

	def form_valid(self, form):
		messages.success(self.request, 'Category updated successfully.')
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('catalog:category-detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
	model = Category
	template_name = 'catalog/category_confirm_delete.html'

	def dispatch(self, request, *args, **kwargs):
		category = self.get_object()
		if category.can_user_manage(request.user):
			return super().dispatch(request, *args, **kwargs)
		raise PermissionDenied

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CategoryDeleteForm(instance=self.object)
		return context

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, 'Category deleted successfully.')
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('catalog:category-list')


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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['reviews'] = (
			Review.objects.select_related('author')
			.filter(game=self.object)
		)
		if self.request.user.is_authenticated:
			context['is_favorite'] = self.object.favorited_by.filter(pk=self.request.user.pk).exists()
			context['my_pending_rental'] = (
				RentalRequest.objects.filter(
					game=self.object,
					borrower=self.request.user,
					status=RentalRequest.Status.PENDING,
				).first()
			)
		return context


class GameCreateView(LoginRequiredMixin, CreateView):
	model = Game
	form_class = GameForm
	template_name = 'catalog/game_form.html'

	def form_valid(self, form):
		form.instance.owner = self.request.user
		messages.success(self.request, 'Game added to the catalog.')
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('catalog:game-detail', kwargs={'pk': self.object.pk})


class GameUpdateView(OwnerOrStaffRequiredMixin, UpdateView):
	model = Game
	form_class = GameForm
	template_name = 'catalog/game_form.html'

	def get_success_url(self):
		return reverse('catalog:game-detail', kwargs={'pk': self.object.pk})

	def form_valid(self, form):
		messages.success(self.request, 'Game details updated.')
		return super().form_valid(form)


class GameDeleteView(OwnerOrStaffRequiredMixin, DeleteView):
	model = Game
	template_name = 'catalog/game_confirm_delete.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = GameDeleteForm(instance=self.object)
		return context

	def get_success_url(self):
		return reverse('catalog:game-list')

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, 'Game deleted from the catalog.')
		return super().delete(request, *args, **kwargs)


class ToggleFavoriteView(LoginRequiredMixin, View):
	def post(self, request, pk: int):
		game = get_object_or_404(Game, pk=pk)
		if game.favorited_by.filter(pk=request.user.pk).exists():
			game.favorited_by.remove(request.user)
		else:
			game.favorited_by.add(request.user)
		return redirect('catalog:game-detail', pk=game.pk)
