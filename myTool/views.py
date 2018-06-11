# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from bs4 import BeautifulSoup
import requests
import json
import re
from django.core import serializers
import nltk
import sys
from nltk.classify import NaiveBayesClassifier
reload(sys)
sys.setdefaultencoding("utf-8")
# from basicapp.models import QueryForm


def index(request):
        posts = 'aazim'  # Getting all the posts from database
        return render(request, 'myTool/post_list.html', { 'posts': posts })

def likePost(request):
    if request.method == 'GET':
		print request.GET.has_key('post_id')
		if request.GET.has_key('post_id'):
			post_id = request.GET['post_id']
			# print '------------------------------',post_id
			likedpost = get_html_tags(str(post_id)) #getting the liked posts
			return HttpResponse(json.dumps({'url':post_id,'tags':likedpost[0], "ids":likedpost[-1]}), content_type="application/json")
		elif request.GET.has_key('url_input'):
			post_id_1 = request.GET['url_input']
			tag_id = request.GET['tag_id']
			main_data = get_selected_tag_data(post_id_1,tag_id)
			# print type(list(main_data))
			return HttpResponse(json.dumps({'html_data':main_data}), content_type="application/json")
    else:
       return HttpResponse("Request method is not a GET")

def get_html_tags(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')
	classes = list(set([value for element in soup.find_all(class_=True) for value in element["class"]]))
	ids = list(set([value for element in soup.find_all(True, {"id":True})]))
	# tags = list(set([tag.name for tag in soup.find_all()]))
	print '-----------------------------------------------------'
	print ids
	# print list(soup(text=re.compile('Technicolor')))
	return classes

def get_selected_tag_data(url,tag):
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')
	# tags = list(set([tag.name for tag in soup.find_all()]))
	# return soup.find_all(tag)
	return list(soup(text=re.compile(tag)))
	# print soup(text=re.compile('exact text'))

def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})