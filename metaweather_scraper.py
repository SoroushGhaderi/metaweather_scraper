import pandas as pd
import datetime 
import requests
import json
import time 

print("Answer questions and complete them then you will recieve csv file, all data available from 2013 to now.")

number_of_cities = int(input("Please enter number of cities that you want: "))

list_of_cities = []
for city in range(number_of_cities):
    city_name = input("Please enter your city name: ")
    list_of_cities.append(city_name)

# Start Date
year_start = int(input("Please input your year of start date: "))
month_start = int(input("Please input your month of start date: "))
day_start = int(input("Please input your day of start date: "))

# End Date
year_end = int(input("Please input your year of end date: "))
month_end = int(input("Please input your month of end date: "))
day_end = int(input("Please input your day of end date: "))

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

start_date = datetime.date(year_start, month_start, day_start)
end_date = datetime.date(year_end, month_end, day_end)
list_of_dates_normal_format = create_range_of_time(start_date, end_date)
list_of_dates_metawheather_format = [loop_date.strftime("%Y/%m/%d") for loop_date in list_of_dates_normal_format]


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
        time.sleep(1)
        print(str(loop_ids), str(loop_date))

list_dict_of_frames = {}
for item in list_of_cities:
    list_dict_of_frames[item] = []

# Create empty list with name of cities that appear in list_of_cities
dict_of_dataframes = {}
for item in list_of_cities:
    dict_of_dataframes[item] = pd.DataFrame()

# add every object of list to dataframe and put it into list of dataframes
for (loop, value), key in zip(list_dict.items(), list_dict_of_frames):
    for number in range(len(list_dict[key])):
        dataframe = pd.DataFrame(value[number])
        clean_dataframe = dataframe.drop(dataframe.index[dataframe["created"].str.slice(start= 0, stop= 10) != dataframe["applicable_date"]])
        list_dict_of_frames[key].append(clean_dataframe)        

for final_dataframe in dict_of_dataframes:
    for frame in list_dict_of_frames:
        dict_of_dataframes[final_dataframe] = pd.concat(list_dict_of_frames[frame], ignore_index= True)
        dict_of_dataframes[final_dataframe].to_csv("{}.csv".format(frame))

