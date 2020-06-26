Metaweather :cloud_with_snow: :sun_behind_small_cloud: :cloud: :sunny: :star: :sun_behind_large_cloud: :snowflake: :fog: :tornado:

MetaWeather provides an API that delivers JSON over HTTPS for access to our data.
This site provides methods as listed below: 

* Location Search
* Find a location
* Location
* Location information, and a 5 day forecast
* Location Day
* Source information and forecast history for a particular day & location

example query record:

URL:
/api/location/search/?query=(query) /api/location/search/?lattlong=(latt),(long)

We find out city id and then query the metaweather with obtained id, after that with pandas library we clean and save tables

**After checking forcast results this script remove them and keep only date weathers.**

**update weather for every station is different some cities updated 3 hours and others may updated 6-8 every hours.**
