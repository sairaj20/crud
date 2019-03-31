from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Metrics(models.Model):
	SCOPE_CHOICES = (
		(None, 'scope default'),
		('private', 'Private'),
		('public', 'Public'),
	)
	name = models.CharField(max_length=80, unique=True)
	title = models.CharField(max_length=200,)
	quantity_name = models.CharField(max_length=80,)
	created_by = models.ForeignKey(User, related_name='%(class)s_created_by', 
		on_delete=models.CASCADE)
	scope = models.CharField(max_length=80, choices=SCOPE_CHOICES)
	duration = models.DurationField()

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Counters(models.Model):
	user = models.ForeignKey(User, related_name='%(class)s_user', 
		on_delete=models.CASCADE)
	metrics = models.ForeignKey(Metrics, related_name='%(class)s_metrics', 
		on_delete=models.CASCADE)
	data_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_on = models.DateTimeField(auto_now_add=True,)

	def __str__(self):
		return str(self.data_value)