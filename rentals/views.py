from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, FormView, ListView

from catalog.models import Game

from .forms import RentalCancelForm, RentalDecisionForm, RentalRequestForm
from .models import RentalRequest
from .tasks import notify_rental_status_change


class RentalRequestCreateView(LoginRequiredMixin, CreateView):
    model = RentalRequest
    form_class = RentalRequestForm
    template_name = 'rentals/rental_request_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['game_pk'])
        if self.game.owner == request.user and not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.game = self.game
        form.instance.borrower = self.request.user
        response = super().form_valid(form)
        notify_rental_status_change.delay(self.object.pk, self.object.status)
        return response

    def get_success_url(self):
        return reverse('rentals:my-requests')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = self.game
        return context


class MyRentalRequestListView(LoginRequiredMixin, ListView):
    model = RentalRequest
    template_name = 'rentals/my_requests.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        status = (self.request.GET.get('status') or '').strip()
        qs = RentalRequest.objects.select_related('game', 'game__owner').filter(borrower=self.request.user)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = (self.request.GET.get('status') or '').strip()
        context['statuses'] = RentalRequest.Status.choices
        return context


class IncomingRentalRequestListView(LoginRequiredMixin, ListView):
    model = RentalRequest
    template_name = 'rentals/incoming_requests.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        status = (self.request.GET.get('status') or '').strip()
        qs = (
            RentalRequest.objects.select_related('game', 'borrower', 'game__owner')
            .filter(game__owner=self.request.user)
        )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = (self.request.GET.get('status') or '').strip()
        context['statuses'] = RentalRequest.Status.choices
        return context


class RentalRequestDetailView(LoginRequiredMixin, DetailView):
    model = RentalRequest
    template_name = 'rentals/rental_request_detail.html'
    context_object_name = 'rental'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.can_user_manage(request.user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class RentalCancelView(LoginRequiredMixin, FormView):
    form_class = RentalCancelForm
    template_name = 'rentals/rental_request_cancel.html'

    def dispatch(self, request, *args, **kwargs):
        self.rental = get_object_or_404(RentalRequest, pk=kwargs['pk'])
        if not (request.user.is_staff or self.rental.borrower == request.user):
            raise PermissionDenied
        if self.rental.status != RentalRequest.Status.PENDING:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.rental
        return kwargs

    def form_valid(self, form):
        self.rental.status = RentalRequest.Status.CANCELLED
        self.rental.decided_at = timezone.now()
        self.rental.save(update_fields=['status', 'decided_at', 'updated_at'])
        notify_rental_status_change.delay(self.rental.pk, self.rental.status)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rentals:my-requests')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental'] = self.rental
        return context


class RentalDecisionView(LoginRequiredMixin, FormView):
    form_class = RentalDecisionForm
    template_name = 'rentals/rental_request_decide.html'

    def dispatch(self, request, *args, **kwargs):
        self.rental = get_object_or_404(RentalRequest, pk=kwargs['pk'])
        if not (request.user.is_staff or self.rental.game.owner == request.user):
            raise PermissionDenied
        if self.rental.status != RentalRequest.Status.PENDING:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        decision = form.cleaned_data['decision']
        self.rental.status = decision
        self.rental.decided_at = timezone.now()
        self.rental.save(update_fields=['status', 'decided_at', 'updated_at'])
        notify_rental_status_change.delay(self.rental.pk, self.rental.status)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rentals:incoming-requests')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental'] = self.rental
        return context
