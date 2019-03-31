from django.urls import path

from . import views

app_name = 'counter'
urlpatterns = [
	# # ex: /polls/
	path('', views.Home.as_view(), name='index'),
	# # ex: /polls/5/
	path('add_counter/<int:metrics_id>/', 
		views.CreateCounter.as_view(), name='add_counter'),
	path('metrics/', 
		views.CreateMetrics.as_view(), name='add_metrics'),
	path('view_counter/<int:metrics_id>/', 
		views.CounterView.as_view(), name='view_counter'),
]