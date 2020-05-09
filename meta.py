import datetime 
import requests
import json
import pandas as pd

year_start = input("Please input your year of start date():")
month_start = input("Please input your month of start date:")
day_start = input("Please input your day of start date:")

year_end = input("Please input your year of end date:")
month_end = input("Please input your month of end date:")
day_end = input("Please input your day of end date:")

# From start_date to end_date create dates and add 1 day for creating list of dates
def create_range_of_time(start_date, end_date, days= 1):
    date = start_date
    list_of_dates = []
    while date != end_date:
        list_of_dates.append(date)
        detla = datetime.timedelta(days)
        date += detla
    return list_of_dates

# Put city name in def and return the id of city
def id_of_city(name_of_city):
    url = "http://www.metaweather.com/api/location/search/?query={}".format(name_of_city)
    response = requests.get(url)
    json_of_response = response.json()
    id_city = json_of_response[0]["woeid"]
    return id_city

start_date = datetime.date(2018, 1, 1)
end_date = datetime.date(2018, 1, 5)
list_of_dates_normal_format = create_range_of_time(start_date, end_date)
list_of_dates_metawheather_format = [loop_date.strftime("%Y/%m/%d") for loop_date in list_of_dates_normal_format]

list_of_cities = ["Chicago", "New York", "Washington"]
# all_ids contains all id of cities in previous list
all_ids = [id_of_city(city) for city in list_of_cities]

# Create empty list with name of cities that appear in list_of_cities
list_dict = {}
for item in list_of_cities:
    list_dict[item] = []

for loop_ids, key in zip(all_ids, list_dict):
    for loop_date in list_of_dates_metawheather_format:
        url = "http://www.metaweather.com//api/location/{}/{}/".format(loop_ids, loop_date)
        response = requests.get(url)
        json_of_response = response.json()
        list_dict[key].append(json_of_response)

list_dict_of_frames = {}
for item in list_of_cities:
    list_dict_of_frames[item] = []

# Create empty list with name of cities that appear in list_of_cities
dict_of_dataframes = {}
for item in list_of_cities:
    dict_of_dataframes[item] = pd.DataFrame()

# add every object of list to dataframe and put it into chicago_frames(all object in chicago_frames are DATAFRAME)
for (loop, value), key in zip(list_dict.items(), list_dict_of_frames):
    for number in range(len(list_dict[key])):
        dataframe = pd.DataFrame(value[number])
        clean_dataframe = dataframe.drop(dataframe.index[dataframe["created"].str.slice(start= 0, stop= 10) != dataframe["applicable_date"]])
        list_dict_of_frames[key].append(clean_dataframe)        

for final_dataframe in dict_of_dataframes:
    for frame in list_dict_of_frames:
        dict_of_dataframes[final_dataframe] = pd.concat(list_dict_of_frames[frame], ignore_index= True)
        dict_of_dataframes[final_dataframe].to_csv("{}.csv".format(frame))

