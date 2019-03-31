from django import forms
from django.conf import settings
from counter.models import *

def get_counter_form(quantity):
	class CounterForm(forms.ModelForm):
		def __init__(self, *args, **kwargs):
			super(CounterForm, self).__init__(*args, **kwargs)
			self.fields['data_value'].label = quantity
			self.fields['user'].widget = forms.HiddenInput()
			self.fields['metrics'].widget = forms.HiddenInput()

		class Meta(object):
			model = Counters
			fields = ('data_value', 'user', 'metrics')

	return CounterForm

class MetricsForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['created_by'].widget = forms.HiddenInput()
		
	class Meta(object):
		model = Metrics
		fields = '__all__'