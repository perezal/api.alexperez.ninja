from django.shortcuts import render
from django.http import HttpResponse

import requests
import os

api_key = os.getenv('TRIMET_API_KEY')

def index(request):

	return render(request, 'trimetApi/index.html')

def arrivals(request, stop_id):

	if request.method == 'GET':
	    url = f'https://developer.trimet.org/ws/V1/arrivals?locIDs={stop_id}&appId={api_key}&json=true&streetcar=true'
	    r = requests.get(url)
	    return HttpResponse(r)

	return HttpResponse('Only accepts GET requests')

def lines(request, line_id=0):

	if request.method == 'GET':
		if line_id == 0:
			url = f'https://developer.trimet.org/ws/V1/routeConfig?appID={api_key}&json=true'
			r = requests.get(url)
			return HttpResponse(r)
		else:
			url = f'https://developer.trimet.org/ws/V1/routeConfig?appID={api_key}&routes={line_id}&dir=true&stops=true&json=true'
			r = requests.get(url)
			return HttpResponse(r)
	return HttpResponse('Only accepts GET requests')

def stops(request, longitude, latitude):

	if request.method == 'GET':
		url = f'https://developer.trimet.org/ws/V1/stops?appID={api_key}&ll={longitude},{latitude}&meters=300&showroutes=true&json=true'
		r = requests.get(url)
		return HttpResponse(r)
	return HttpResponse('Only accepts GET requests')

