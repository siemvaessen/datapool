from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import DollyData,TwitterUser
from django.db.models import Count
import json

# Create your views here.


def get_dolly_data(request):

	start_date = request.GET['start']
	end_date = request.GET['end']
	exclude_ids = []
	
	exclude_ids = request.GET.getlist('exclude_ids')
	include_ids = request.GET.getlist('include_ids')

	if 'search' in request.GET and request.GET['search'] != '':
		search_string = request.GET['search']
		data = DollyData.objects.filter(create_at__range=[start_date, end_date]).filter(text__search=search_string).exclude(u_id_id__in=exclude_ids)[:1000]
	else:
		data = DollyData.objects.filter(create_at__range=[start_date, end_date]).exclude(u_id_id__in=exclude_ids)[:1000]
	return HttpResponse(serializers.serialize("json", data))

def get_tweets_per_day(request):
	start_date = request.GET['start']
	end_date = request.GET['end']
	start_date = request.GET['start']
	end_date = request.GET['end']
	if 'search' in request.GET and request.GET['search'] != '':
		search_string = request.GET['search']
		data = DollyData.objects.filter(create_at__range=[start_date, end_date]).filter(text__search=search_string).extra(select={'day': 'date( create_at )'}).values('day').annotate(tweets=Count('create_at')).order_by('day')
	else:
		data = DollyData.objects.filter(create_at__range=[start_date, end_date]).extra(select={'day': 'date( create_at )'}).values('day').annotate(tweets=Count('create_at')).order_by('day')
	return_data = []
	for row in  data:
		return_data.append({'tweets':row['tweets'],'date': str(row['day'])})
	return HttpResponse(json.dumps(return_data))

def get_top_twitter_users(request):
	data = TwitterUser.objects.all().order_by('-count')[:50]
	return HttpResponse(serializers.serialize("json", data))
