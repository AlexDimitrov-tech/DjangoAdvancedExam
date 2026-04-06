from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from .forms import ProfileEditForm, SignUpForm
from .models import CustomUser


class SignUpView(FormView):
	template_name = 'accounts/signup.html'
	form_class = SignUpForm

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['recent_notifications'] = self.request.user.notifications.select_related('rental_request', 'rental_request__game')[:5]
		return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
	model = CustomUser
	form_class = ProfileEditForm
	template_name = 'accounts/profile_edit.html'
	success_url = reverse_lazy('accounts:profile')

	def get_object(self, queryset=None):
		return self.request.user

	def form_valid(self, form):
		messages.success(self.request, 'Profile updated.')
		return super().form_valid(form)
