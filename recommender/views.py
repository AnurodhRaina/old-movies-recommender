from django.shortcuts import render
from django.http import HttpResponse
from pandas import read_csv
# Create your views here.

import os
# for cosine metric
from scipy.sparse import save_npz, load_npz
import pickle
from pandas import read_csv
from sklearn.metrics.pairwise import cosine_similarity
import json

# for image covers
from bs4 import BeautifulSoup
import urllib
import requests
from PIL import Image


'''=======================VIEWS HERE========================'''


def info(request):
    return render(request,'recommender/info.html')

def dashboard(request):
    return render(request,'recommender/dashboard.html')

def Table(request):
    df = read_csv("static/csv/movie_plots.csv")
    #'tableview/static/csv/movie_plots.csv' is the django 
    # directory where csv file exist.
    # Manipulate DataFrame using to_html() function as an alternative

    # loading the vector for the comparison using cosine similarity
    vector = load_npz('static/npz/vectorized_plots_2.npz')

    a = pickle.load(open('static/pkl/vector_2.pkl', 'rb'))
    #with open('static/pkl/vector_2.pkl', 'rb') as vectorizer:
      #a = pickle.load(vectorizer)

      # loading the pickle file 
      # in order to have it as a transformer for the query text
    
    input_string = request.GET.get('movie_query')
    # the users input to the text field

    #sample_vector = a.transform([input_string])
    # the vectorizer that transform according to the dataset

    #var = cosine_similarity(vector, a.transform([input_string]))
    # calculating the similarity score 

    df['Cosine'] = cosine_similarity(vector, a.transform([input_string]).astype('float16'))
    # storing the score array
    
    df = df.sort_values(by = 'Cosine', ascending = False)[:10]

    links = [i for i in df['Wiki_Page']] # wikipedia pages for images
    
    images = []
    for link in links:
        r = requests.get(link) # URL to these links
        soup = BeautifulSoup(r.content, features="html.parser")# using soup to parse
        covers = soup.select('table.infobox a.image img[src]') # se;ecting the img src tag
        
        try:
            full_link = 'https:' + covers[0]['src']
        except:
            full_link = 'Image Not found'
            pass
        # the actual link that can be read by PIL as an image

        #image_url_to_read = urllib.request.urlretrieve(full_link)[0]
        #path = 'static/img/'
        #full_path = os.path.join(path, full_link)
        #urllib.request.urlretrieve(full_link, full_path)
        #img = Image.open(image_url_to_read)
        # reading the image
        images.append(full_link)
        # appending it to the dataframe

    df['Cover'] = images
    # sorting to get thehighest scores i.e. the most similar instances
   
    #json_records = df.reset_index(drop = True).to_json(orient ='records')
    data = json.loads(df.reset_index(drop = True).to_json(orient ='records'))
    context = {'d': data}
    # displaying the most similar data
    
    return render(request, 'recommender/info.html', context)


# Create your views here.
