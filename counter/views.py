from django.shortcuts import render
from django.db.models import Q 
from django.views.generic import TemplateView
from django.utils import timezone
from django.urls import reverse_lazy 
from counter.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from .forms import *
from django.core.exceptions import PermissionDenied



class CreateMetrics(LoginRequiredMixin, CreateView):
	model = Metrics
	template_name = 'counter/create_metrics.html'
	success_url = reverse_lazy('counter:index')
	form_class = MetricsForm

	def get_initial(self):
		return {'created_by':self.request.user,}

class CreateCounter(LoginRequiredMixin, CreateView):
	model = Counters
	template_name = 'counter/create_counter.html'
	success_url = reverse_lazy('counter:index')
	
	def get_form_class(self):
		return get_counter_form(self.metrics.quantity_name)

	def get_initial(self):
		return {
			'user':self.request.user,
			'metrics':self.metrics
		}

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['metrics'] = self.metrics
		return context

	def get(self, request, metrics_id, *args, **kwargs):
		self.metrics = Metrics.objects.get(pk=metrics_id)
		counter = Counters.objects.filter(
			metrics=self.metrics, 
			user=self.request.user
		)
		if not counter.exists() or counter.exists() and (timezone.now() - counter.last().created_on) >= self.metrics.duration:
			return super().get(request, *args, **kwargs)
		else :
			raise PermissionDenied

	def post(self, request, metrics_id, *args, **kwargs):
		self.metrics = Metrics.objects.get(pk=metrics_id)
		return super().post(request, *args, **kwargs)

class CounterView(LoginRequiredMixin, TemplateView):
	template_name = 'counter/counter_view.html'

	def get(self, request, metrics_id, *args, **kwargs):
		self.metrics = Metrics.objects.get(pk=metrics_id)
		return super().get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['metrics'] = self.metrics
		context['user_counters'] = Counters.objects.filter(user=self.request.user,metrics=self.metrics)

		return context

class Home(LoginRequiredMixin, TemplateView):
	template_name = 'counter/home.html'
	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		metrics = Metrics.objects.filter(
			Q(created_by=self.request.user)|
			Q(scope='public')|
			Q(scope__isnull=True)
		)
		metrics_list = []
		for x in metrics.iterator():
			counter = Counters.objects.filter(
				metrics=x, 
				user=self.request.user
			)
			if not counter.exists() or counter.exists() and (timezone.now() - counter.last().created_on) >= x.duration:
				metrics_list.append(x)

		context['metrics_list'] = metrics_list
		context['all_metrices'] = metrics 
		return context
