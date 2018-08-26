import sys
import csv
import pandas as pd
import re
from datetime import datetime as dt
import datetime
import numpy as np
import collections
import operator
from django.contrib.auth.models import User
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesis_project.settings')
django.setup()
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def getRandomTweets(request):
    tweets_list = list()
    data = MinedTweet.objects.values().order_by('-date')[:10]
    for entry in data:
        tweets_list.append([entry['tweet'], entry['username'], 'random'])
    return JsonResponse({'data': tweets_list})

def getProduct(request):
    product_list = list()
    products= Product.objects.values()
    for product in products:
        product_list.append(product['name'])
    return JsonResponse({'data': product_list})

def setProduct(request):
    if request.method == 'POST':
        data = request.data
        product = Product.objects.get_or_create(name = data.name)
    return JsonResponse({'data': 'success'})

def setFarmerProduct(request):
    if request.method == 'POST':
        data = request.data
        farmer = Farmer.objects.get_or_create(name = data.name)
        farmer.save()
        product = Product.objects.get_or_create(name = data.product)
        product.save()
        farmerProduct = FarmerProduct(product, farmer, data.description)
    return JsonResponse({'data': 'success'})

def setFarmer(request):
    if request.method == 'POST':
        data = request.data
        coordinates = Coordinate.objects.get_or_create(lng = data.address.lng, lat = data.address.lat)
        address = Address.objects.get_or_create(coordinates, city, pllace)
        farmer = Farmer.objects.get_or_create(address, name = data.name)
        farmer.save()

    return JsonResponse({'data': 'success'})

def get_report(request):
    tweet = get_ill_tweets()
    return JsonResponse({'data': tweet})

def get_number_tweet(request):
    return JsonResponse(label_count_result())

#  private function
today = dt.today()
categories_dict = {'Concerns': 0,'Issues': 1,'bigas': 2,'ampalaya': 3
                                ,'kamatis': 4,'pipino': 5,'saging': 6,'pinya': 7,'pineapple': 8
                                ,'abaca fiber': 9,'cabbage': 10,'news': 11,'kamote': 12}

categories = list(categories_dict.keys())

def label_count_result():
    label = dict()
    num_random_tweets = MinedTweet.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day).count()
    label['total'] = num_random_tweets
    svm = process_svm()
    test_model = get_test_data()
    if test_model != None:
        num_illness_tweets = len(test_model['test_model'])
        label['total'] += num_illness_tweets

        predicted = svm.predict(test_model['test_model'])
        counter = collections.Counter(predicted)
        for key in counter:
            label[categories[key]] = counter[key]

        sorted_x = sorted(label.items(), key=operator.itemgetter(1))
        label = dict(sorted_x[-5:])

    return label

def get_stop_words(X,y):
    custom_words = StopWord.objects.values()
    stop_words = [entry['words'] for entry in custom_words]

    vect = CountVectorizer(analyzer='word',
                            stop_words='english'
                            )
    vect.fit(X,y)
    feature_names = vect.get_feature_names()
    for word in feature_names:
        if len(word) < 4:
            stop_words.append(word)
    return stop_words

def process_svm():
    tweets_obj = { }
    model = TrainModel.objects.values()
    list_t = [entry['tweet'] for entry in model]
    list_l = [entry['label'] for entry in model]
    my_dict = { "tweet": list_t, "label": list_l }

    df = pd.DataFrame(data = my_dict)
    df['label_num'] = df.label.map(categories_dict)
    df['label_num'] = df['label_num'].values.astype(np.int64)

    X_model = df.tweet
    y_model = df.label_num

    custom_stop_words = get_stop_words(X_model, y_model)

    text_clf = Pipeline(steps=[('vect', CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS.union(custom_stop_words))),
                        ('tfidif', TfidfTransformer()),
                        ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                alpha=1e-3,
                                                max_iter=5, tol=None)),
                        ])

    text_clf.fit(X_model, y_model)
    return text_clf

def get_test_data():
    model = Tweet.objects.all()

    if len(model) > 0:
        list_t = [entry.tweet for entry in model]
        my_dict = { "tweet": list_t}
        df_test = pd.DataFrame(data = my_dict)

        for idx, val in enumerate(df_test['tweet']):
            df_test['tweet'][idx] = clear_texting(val)

        X_Test_Model = df_test.tweet
        origin = list_t
        return {'test_model': X_Test_Model, 'tweets': list_t, 'data': model}

    return None

def clear_texting(string):
    first_filter = remove_tags(string)
    # remove links
    second_filter = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', first_filter)
    # remove symbols
    return re.sub(r'[^\w]', ' ', str(second_filter.lower()))

def remove_tags(string):
    tweet = string
    stopper = 0
    while(tweet.find('@') != -1):
        tag_index = tweet.find("@")
        end_of_tag_index = tweet[tag_index:].find(" ")

        # this will concatinate the text with their indexes without the tag
        tweet = tweet[:tag_index] + tweet[(tag_index+end_of_tag_index):] if end_of_tag_index != -1 else tweet[:tag_index]

    return tweet

def get_ill_tweets():
    svm = process_svm()
    model = get_test_data()
    tweets_list = []
    if model != None:
        predicted = svm.predict(model['test_model'])
        for tweets, label, entity in zip(model['tweets'], predicted, model['data']):
            tweets_list.append([tweets, entity.coordinates.lat, entity.coordinates.lng, categories[label]])
            # if entity.isTrained == None:
            #     add_train_data(tweets, categories[label])

    return tweets_list
