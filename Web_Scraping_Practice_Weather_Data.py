"""
Created on Fri Jun  1 15:16:53 2018
@author: kmuss

This program scrapes weather data from weather.gov. 
I followed the following tutorial as I was learning how to scrape web pages. 
Tutorial: https://www.dataquest.io/blog/web-scraping-tutorial-python/
"""
import requests
from bs4 import BeautifulSoup

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.WxgqgUgvyUl")
soup = BeautifulSoup(page.content, 'html.parser')
soup.find(id="seven-day-forecast")

# Now let's print out tonight's weather. 
""" Note - the tutorial uses tonights data, but weather forecast is now set to day, please 
ignore any discrepancies between "tonight" and "today". """

seven_day = soup.find(id="seven-day-forecast")
# separate forecast into individual days
forecast_items = seven_day.find_all(class_="tombstone-container")
# tonight should be the first item in the forecast
tonight = forecast_items[0]
print(tonight.prettify())

#extract the name of what we're looking at ("Today")
period = tonight.find(class_="period-name").get_text()
#period

# extract the short description text
short_desc = tonight.find(class_="short-desc").get_text()

## extract tonight's high/low temperature 
temp = tonight.find(class_='temp temp-low').get_text()

#print all extracted information to this point. Print statements may be grayed out - used for testing purposes. 
#print(period)
#print(short_desc)
#print(temp)

## Extract the long description - from an img
img = tonight.find("img")
desc = img['title']
print(desc)
           
# EXTRACT ALL THE INFO FROM THE PAGE 
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
periods 

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

#print(short_descs)
#print(temps)
#print(descs)

## PUT THIS DATA INTO A PANDAS DATAFRAME
import pandas as pd
weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs,
        "temp": temps, 
        "desc": descs
        })
weather 

# NOW WE CAN DO ANALYSIS 
# Extract the temperatures from this data as a Series
temp_nums = weather["temp"]
#print(temp_nums)

#the temp column is composed of strings - "high" and "low" are in it. 
# extract only the #'s and convert to ints
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
#print(temp_nums)

#Find the mean temp 
print(weather["temp_num"])
print("")
print(weather["temp_num"].mean())

## Select only the rows that happen at night: 
# First, create a boolean series for if the low temp is listed
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
is_night

weather[is_night]
