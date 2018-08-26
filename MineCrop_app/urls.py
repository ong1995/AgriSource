from django.urls import path
from django.conf.urls import url
from MineCrop_app import views

app_name = 'minecrop_app'
urlpatterns = [
    path('getRandomTweets', views.getRandomTweets),
    path('getProduct', views.getProduct),
    path('get_report', views.get_report),
    path('get_number_tweet', views.get_number_tweet),
    path('setProduct', views.setProduct),
    path('setFarmerProduct', views.setFarmerProduct),
    path('setFarmer', views.setFarmer),
]
