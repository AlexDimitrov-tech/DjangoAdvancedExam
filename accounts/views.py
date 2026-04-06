from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from .forms import SignUpForm


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
