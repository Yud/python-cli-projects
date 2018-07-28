# -*- coding: utf-8 -*-

import requests
import re
import datetime
import time
import click
import sys

URL = "https://www.10bis.co.il/Restaurants/SearchRestaurants"

searchParams = {
    'deliveryMethod': 'Delivery',
    'ShowOnlyOpenForDelivery': 'False',
    'pageNum': 0,
    'pageSize': 50,
    'OrderBy': 'pool_sum',
    'cuisineType': '',
    'CityId': 0,
    'StreetId': 0,
    'FilterByKosher': 'false',
    'FilterByCoupon': 'false',
    'Latitude': 32.061711,
    'Longitude': 34.788543000000004, 
    'HouseNumber': 1
}

def match_emojis(food_list):
    emojis = []
    for food in food_list.split(','):
        f = food.encode('utf-8')
        if (re.search("סושי", f)):
            emojis.append(u'🍣'.encode('utf-8'))
        if (re.search("סלט", f)):
            emojis.append(u'🥗'.encode('utf-8'))
        if (re.search("בשר", f)):
            emojis.append(u'🍗'.encode('utf-8'))
        if (re.search("איטלקי", f)):
            emojis.append(u'🍝'.encode('utf-8'))
        if (re.search("אסייתי", f)):
            emojis.append(u'🍜'.encode('utf-8'))
        if (re.search("סנדוויצ", f)):
            emojis.append(u'🥪'.encode('utf-8'))
    return ' '.join(emojis)

def fetch_orders(id):
    desired_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    searchParams.update({'desiredDateAndTime': desired_time, 'id': id})
    orders = requests.get(URL, params=searchParams)
    orders_list = orders.json()
    for order in orders_list[:8]:
        name = order['RestaurantName'][::-1].encode('utf-8')
        emjs = match_emojis(order['RestaurantCuisineList'])
        total_orders_sum = order['PoolSumNumber']
        over_min = order['IsOverPoolMin']
        color = 'green' if over_min == 'True' else 'white'
        output = '{} {} {}'.format(total_orders_sum, name, emjs)
        click.secho(output, fg=color)

@click.command()
@click.option('--id', default=1, help='10Bis user id')
def main(id):
    while True:
        try:
            click.clear()
            fetch_orders(id)
            time.sleep(30)
        except KeyboardInterrupt:
            print "Bye"
            sys.exit()

if __name__ == '__main__':
    main()
