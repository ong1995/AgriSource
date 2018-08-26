import sys
import tweepy
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MineCrop.settings')
django.setup()
import sqlite3
from MineCrop_app.models import *
conn = sqlite3.connect('db.sqlite3')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')
c = Coordinate.objects.get_or_create(lng = 125.607823, lat = 7.062365)[0]
c.save()
t = Tweet.objects.get_or_create(coordinates = c, userid = 100006, name = "Ian Troy",
tweet = "saan makabili ng abaca fiber?",
                                location = "davao")[0]
t.save()

c = Coordinate.objects.get_or_create(lng = 125.617774, lat = 7.081279)[0]
c.save()
t = Tweet.objects.get_or_create(coordinates = c, userid = 100007, name = "Peter Duot",
tweet = "naghahanap po kami ng abaca fiber. Sino po nakakaalam saan?",
                                location = "davao")[0]
t.save()

c = Coordinate.objects.get_or_create(lng = 125.616099, lat = 7.080881)[0]
c.save()
t = Tweet.objects.get_or_create(coordinates = c, userid = 100008, name = "Dodo J",
tweet = "WHERE CAN WE BUY ABACA FIBER IN METRO MANILA?",
                                location = "davao")[0]
t.save()
# Insert a row of data
# c.execute("INSERT INTO MineCrop_app_trainmodel VALUES (90,'kamote','FOR SALE: kamote, newly harvested ito...  San Carlos City, Pangasinan ang location ')")
# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
