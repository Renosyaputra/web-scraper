import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'courses/index.html')

def new_search(request):

    # Catching user input & feeding that to Search table in models 
    keyword = request.POST.get('keyword')
    models.Search.objects.create(search=keyword)

    # Reforming the carigslist URL by adding the user input in the bracket part
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(keyword))
    response = requests.get(final_url)

    # Calling the html parser from BeautifulSoup library
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    # Parsing the <li> tag to get the class result-title and <a href=""> and store it in final_posting 
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_= 'result-title').text
        post_datetime = post.find('time').get('title')
        post_url = post.find('a').get('href')
        
        if post.find(class_= 'result-image').get('data-ids'):
            post_image_id = post.find(class_= 'result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'null'
        
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price')
        else:
            post_price = 'null'

        final_postings.append((post_title, post_datetime, post_image_url, post_url, post_price))

    search_keyword = {
        'keyword' : keyword,
        'final_postings' : final_postings,
    }
    return render(request, 'courses/new_search.html', search_keyword)
