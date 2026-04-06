from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from catalog.models import Game

from .forms import ReviewDeleteForm, ReviewForm
from .models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['game_pk'])
        if self.game.owner == request.user and not request.user.is_staff:
            messages.info(request, 'You cannot review your own game listing.')
            return redirect('catalog:game-detail', pk=self.game.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.game = self.game
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:game-detail', kwargs={'pk': self.game.pk})


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.select_related('author', 'game', 'game__owner')


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_staff or obj.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_success_url(self):
        return reverse('catalog:game-detail', kwargs={'pk': self.object.game.pk})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_staff or obj.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewDeleteForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse('catalog:game-detail', kwargs={'pk': self.object.game.pk})
