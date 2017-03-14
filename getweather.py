#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :
'''
Get weather from weather underground
Using hourly weather prediction, almanac
@author: amr1990
'''

import sys
import requests
import json

api_key = None  # If assigned won't read argv[1]


class WeatherClient(object):

    """Will access weatherunderground to gather weather information
    Provides access to wunderground API
    (http://www.wunderground.com/weather/api)
    Provides methods:
        almanac
    """

    url_base = 'http://api.wunderground.com/api/'
    url_services = {
        "almanac": "/almanac/q/CA/",
        "hourly" : "/hourly/q/CA/"
    }

    def __init__(self, apikey):
        super(WeatherClient, self).__init__()
        self.api_key = apikey


    def hourly(self, location="Lleida"):
        """
        Accesses weatherunderground hourly information for the given location
        """
        resp_format = "json"
        url = WeatherClient.url_base + api_key + WeatherClient.url_services["hourly"] + location + "." + resp_format
        r = requests.get(url)

        jsondata = json.loads(r.text)
        return jsondata["hourly_forecast"]

    def almanac(self, location="Lleida"):
        """
        Accesses wunderground almanac information for the given location
        """
        resp_format = "json"
        url = WeatherClient.url_base + api_key + WeatherClient.url_services["almanac"] + location + "." + resp_format
        r = requests.get(url)

        jsondata = json.loads(r.text)
        return jsondata["almanac"]


def print_hourly(hourly_prediction, interval=1):
    """
    Prints for a given interval the hourly forecast
    """
    rain = 0
    temp = 0
    for i in range(0, interval):
        print "-------------------------------------------------------"
        print "Forecast for %s" % (hourly_prediction[i]["FCTTIME"]["pretty"])
        print "Condition: %s" % (hourly_prediction[i]["condition"])
        print "Temperature: %s C" % (hourly_prediction[i]["temp"]["metric"])
        print "Thermal sensation: %s C" % (hourly_prediction[i]["feelslike"]["metric"])
        print "Wind speed: %s Km/h" % (hourly_prediction[i]["wspd"]["metric"])
        print "Wind direccion: %s degrees, direction: %s" % (hourly_prediction[i]["wdir"]["degrees"], hourly_prediction[i]["wdir"]["dir"])
        print "Humidity: %s %%" % (hourly_prediction[i]["humidity"])
        print ""
        print "Clothing advise:"

        rain = rain + int(hourly_prediction[i]["fctcode"])
        temp = temp + int(hourly_prediction[i]["temp"]["metric"])

    avgrain = rain / interval
    avgtemp = temp / interval

    if 10 <= avgrain <= 12:
        print "Think about bringing an unbrella"

    if 13 <= avgrain <= 15:
        print "IT'S RAINING MAN. HALLELUJAH!!!!"

    if avgtemp >= 25:
        print "It's going to be a hot day. It's time to wear summer clothes"

    if 15 < avgtemp < 25:
        print "It's going to be a cold day. Think about bring a jacket"

    if avgtemp < 15:
        print "It's going to be a typical winter day. It's time to wear winter clothes"

    print "-------------------------------------------------------"


def print_almanac(almanac):
    """
    Prints an almanac received as a dict
    """
    print "High Temperatures:"
    print "Average on this date", almanac["temp_high"]["normal"]["C"]
    print "Record on this date %s (%s) " % \
        (almanac["temp_high"]["record"]["C"],
            almanac["temp_high"]["recordyear"])
    print "Low Temperatures:"
    print "Average on this date", almanac["temp_low"]["normal"]["C"]
    print "Record on this date %s (%s) " % \
        (almanac["temp_low"]["record"]["C"],
            almanac["temp_low"]["recordyear"])


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "Must provide api key in code or cmdline arg"

    location = raw_input("Enter location: ")

    try:
        interval = int(raw_input("Enter a time interval for the weather forecast: "))
    except ValueError:
        print "Not a number"
        sys.exit()

    weatherclient = WeatherClient(api_key)
    print_hourly(weatherclient.hourly(location), interval)
