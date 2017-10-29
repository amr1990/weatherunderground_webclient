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
import gettext
import os

api_key = None  # If assigned won't read argv[1]


class WeatherClient(object):

    """Will access weatherunderground to gather weather information
    Provides access to wunderground API
    (http://www.wunderground.com/weather/api)
    Provides methods:
        almanac
        hourly
    """

    url_base = 'http://api.wunderground.com/api/'
    url_services = {
        "almanac": "/almanac/q/CA/",
        "hourly" : "/hourly/q/CA/"
    }

    def __init__(self, apikey):
        super(WeatherClient, self).__init__()
        self.api_key = apikey

    @staticmethod
    def hourly(location="Lleida"):
        """
        Accesses weatherunderground hourly information for the given location
        """
        resp_format = "json"
        url = WeatherClient.url_base + api_key + WeatherClient.url_services["hourly"] + location + "." + resp_format
        r = requests.get(url)

        jsondata = json.loads(r.text)
        return jsondata["hourly_forecast"]

    @staticmethod
    def almanac(location="Lleida"):
        """
        Accesses wunderground almanac information for the given location
        """
        resp_format = "json"
        url = WeatherClient.url_base + api_key + WeatherClient.url_services["almanac"] + location + "." + resp_format
        r = requests.get(url)

        jsondata = json.loads(r.text)
        return jsondata["almanac"]


def print_hourly(hourly_prediction, interval):
    """
    Prints for a given interval the hourly forecast
    """
    rain = 0
    temp = 0
    for i in range(0, interval):
        print "-------------------------------------------------------"
        print _("Forecast for"), str(hourly_prediction[i]["FCTTIME"]["pretty"])
        print _("Condition:"), str(hourly_prediction[i]["condition"])
        print _("Temperature:"), str(hourly_prediction[i]["temp"]["metric"]), _("C")
        print _("Thermal sensation:"), (hourly_prediction[i]["feelslike"]["metric"]), _("C")
        print _("Wind speed:"), str(hourly_prediction[i]["wspd"]["metric"]), _("Km/h")
        print _("Wind direccion:"), str(hourly_prediction[i]["wdir"]["degrees"]), _("degrees, direction:"), str(hourly_prediction[i]["wdir"]["dir"])
        print _("Humidity:"), str(hourly_prediction[i]["humidity"]), _("%")
        print ""
        print _("Clothing advise:")

        rain = rain + int(hourly_prediction[i]["fctcode"])
        temp = temp + int(hourly_prediction[i]["temp"]["metric"])

    avgrain = rain / interval
    avgtemp = temp / interval

    if 10 <= avgrain <= 12:
        print _("Think about bringing an unbrella")

    if 13 <= avgrain <= 15:
        print _("IT'S RAINING MAN. HALLELUJAH!!!!")

    if avgtemp >= 25:
        print _("It's going to be a hot day. It's time to wear summer clothes")

    if 15 < avgtemp < 25:
        print _("It's going to be a cold day. Think about bring a jacket")

    if avgtemp < 15:
        print _("It's going to be frosty. It's time to wear winter clothes")

    print "-------------------------------------------------------"


def print_almanac(almanac):
    """
    Prints an almanac received as a dict
    """
    print _("High Temperatures:")
    print _("Average on this date:"), str(almanac["temp_high"]["normal"]["C"])
    print _("Maximum on this date:"), str(almanac["temp_high"]["record"]["C"]), _("("), str(almanac["temp_high"]["recordyear"]), _(")")
    print _("Low Temperatures:")
    print _("Average on this date:"), str(almanac["temp_low"]["normal"]["C"])
    print _("Minumum on this date:"), str(almanac["temp_low"]["record"]["C"]), _("("), str(almanac["temp_low"]["recordyear"]), _(")")


if __name__ == "__main__":
    appdir = os.path.dirname(sys.argv[0])
    appdir = os.path.abspath(appdir)
    localedir = os.path.join(appdir, "locales")

    gettext.install("getweather", localedir)

    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print _("Must provide api key in code or cmdline arg")

    location = raw_input(_("Enter location: "))

    try:
        interval = int(raw_input(_("Enter a time interval for the weather forecast: ")))
    except ValueError:
        print _("Not a number")
        sys.exit()

    weatherclient = WeatherClient(api_key)
    print_hourly(weatherclient.hourly(location), interval)
    print_almanac(weatherclient.almanac(location))
