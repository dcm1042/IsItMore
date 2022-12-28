import time

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pairs
import random
import requests

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import openai
from django import forms

class HomepageView(LoginRequiredMixin, TemplateView):
	template_name = 'index.html'
	login_url = '/auth/login/'
	redirect_field_name = 'redirect_to'
	data = {}
	voted = False

	def post(self, request, *args, **kwargs):
		global data
		global voted
		if self.request.POST.get('btn') == 'next':

			data = Pairs.objects.values()
			data = data[random.randint(0, len(data) - 1)]
			response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
				'option1'] + "&image_type=photo")
			data['image1'] = response.json()['hits'][1]['webformatURL']
			response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
				'option2'] + "&image_type=photo")
			data['image2'] = response.json()['hits'][1]['webformatURL']
			data['votes1text'] = ""
			data['votes2text'] = ""
			data['nxtbtn'] = 'none'
			voted = False
			return render(request, self.template_name, data)
		if not voted:
			data['nxtbtn'] = "inline"
			if self.request.POST.get('btn') == 'option1':
				Pairs.objects.filter(id=data['id']).update(votes1= F('votes1') + 1)

			elif self.request.POST.get('btn') == 'option2':
				Pairs.objects.filter(id=data['id']).update(votes2= F('votes2') + 1)

			id = int(data['id'])

			data = Pairs.objects.values()
			for question in data:
				if question['id'] == id:
					data = question
					break;


			response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
				'option1'] + "&image_type=photo")
			data['image1'] = response.json()['hits'][1]['webformatURL']
			response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
				'option2'] + "&image_type=photo")
			data['image2'] = response.json()['hits'][1]['webformatURL']
			data['votes1text'] = "Votes: "+str(data['votes1'])
			data['votes2text'] = "Votes: "+str(data['votes2'])
			voted = True
		return render(request, self.template_name, data )

		'''
		data = Pairs.objects.values()
		data = data[random.randint(0, len(data) - 1)]
		option1 = data['option1']
		option2 = data['option2']
		args = {'option1': option1, 'option2': option2}
		print(self.request.POST.get('btn'))
		response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
			'option1'] + "&image_type=photo")
		data['image1'] = response.json()['hits'][1]['webformatURL']
		response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
			'option2'] + "&image_type=photo")
		data['image2'] = response.json()['hits'][1]['webformatURL']
		'''


	def test(self):


		return render(self,'../templates/index.html',)


	def get_context_data(self, **kwargs):
		global data
		global voted
		voted = False

		data = Pairs.objects.values()
		data = data[random.randint(0, len(data)-1)]
		option1 = data['option1']
		data['nxtbtn'] = "none"

		option2 = data['option2']
		args = {'option1': option1, 'option2': option2}
		'''
			response = openai.Image.create(
				prompt=data['option1'],
				n=1,
				size="256x256"
			)
			
			
			data['image1'] = response['data'][0]['url']
			response = openai.Image.create(
				prompt=data['option2'],
				n=1,
				size="256x256"
			)
			data['image2'] = response['data'][0]['url']
			'''
		response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q="+data['option1']+"&image_type=photo")
		data['image1'] = response.json()['hits'][1]['webformatURL']
		response = requests.get("https://pixabay.com/api/?key=32393549-bf26b1528d5dd1007ed9eb0ef&q=" + data[
			'option2'] + "&image_type=photo")
		data['image2'] = response.json()['hits'][1]['webformatURL']
		data['votes1text'] = ""
		data['votes2text'] = ""
		return data

