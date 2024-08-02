import os
import http.client
import json
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Weather_hourly, Weather_daily, Weather_monthly



def load_credentials() : 
    file_path = os.path.join(os.path.dirname(__file__), 'credentials.txt')
    try :
        dict_credentials = {}
        with open(file_path,'r') as file :
            
            for line in file :
                key,value = line.split(':')
                dict_credentials [key] = value.rstrip('\n')
                
    except FileNotFoundError : 
        print("file not found!")
    
    finally : 
        return dict_credentials
                  
conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")      
credentials = load_credentials() 
print(credentials)

    
headers = {
    'x-rapidapi-key': credentials['x-rapidapi-key'],
    'x-rapidapi-host': credentials['x-rapidapi-host'] 
}


def get_weather (connection, interval , start_date, end_date) :

    weather_info ={}
    try: 
        
        if (interval == "hourly") : 
            connection.request("GET", f"/stations/{interval}?station=10637&start={start_date}&end={end_date}&tz=Europe%2FBerlin", headers=headers)
            res = conn.getresponse()
            data = res.read()
            weather_data = json.loads(data.decode("utf-8"))
            json_list = weather_data['data']
            json.loads(json.dumps(json_list), object_hook=Weather_hourly.weather_custom_decoder) 
            weather_info = [Weather_hourly(**data) for data in json_list]
            #print(weather_info)
            
        elif (interval == "daily"):
            connection.request("GET", f"/stations/{interval}?station=10637&start={start_date}&end={end_date}", headers=headers)
            res = conn.getresponse()
            data = res.read()
            weather_data = json.loads(data.decode("utf-8"))
            json_list = weather_data['data']
            json.loads(json.dumps(json_list), object_hook=Weather_daily.weather_custom_decoder) 
            weather_info = [Weather_daily(**data) for data in json_list]
            #print(weather_info)
            
        elif (interval == "monthly"): 
           # conn.request("GET", "/stations/monthly?station=10637&start=2020-01-01&end=2020-12-31", headers=headers)

            connection.request("GET", f"/stations/{interval}?station=10637&start={start_date}&end={end_date}", headers=headers)
            res = conn.getresponse()
            data = res.read()
            weather_data = json.loads(data.decode("utf-8"))
            json_list = weather_data['data']
            json.loads(json.dumps(json_list), object_hook=Weather_monthly.weather_custom_decoder) 
            weather_info = [Weather_monthly(**data) for data in json_list]
            #print(weather_info)
            
        
    except ConnectionError : 
        print(f"unable to connect! {ConnectionError}")
    finally : 
            return weather_info; 
        
        
#Interval : hourly[entire day], daily[entire month], monthly [entire year] 
'''
interval = "hourly"  
start_date="2024-07-01" 
end_date="2024-07-01"

interval = "daily"  
start_date="2024-01-01" 
end_date="2024-01-31"
#conn.request("GET", "/stations/daily?station=10637&start=2020-01-01&end=2020-01-31", headers=headers)
'''
'''
interval = "monthly"  
start_date="2024-01-01" 
end_date="2024-12-31"
#conn.request("GET", "/stations/monthly?station=10637&start=2020-01-01&end=2020-12-31", headers=headers)
'''        
    
def filter_hourly_weather(weather_data:Weather_hourly ): 

    try:
        return [daily for daily in weather_data if daily.time >= datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    except TypeError:
        print("Error: No data.")
        return []
    
def filter_daily_weather(weather_data:Weather_daily):
    week_weather = []
    print(weather_data)
    try:
        for weather in range(6):
            week_weather.append(weather_data[weather])
    except IndexError :
        print("Error: Not enough data for 7 days.")
    except KeyError:
        print("Error : No weather data.")
    return week_weather


def filter_monthly_weather(weather_data:Weather_monthly ): 
    if  ( weather_data.date < (datetime.now().strftime('%Y-%m-%d %H:%M:%S') ) )  and weather_data.tavg != None  : 
        return weather_data
    
# Create your views here.
def home(request): 
    
   now = datetime.now()
   
   start_date = now.strftime('%Y-%m-%d')
   
   

   start_time = now.strftime('%H:%M:%S')
   
   
   hourly = get_weather (conn, "hourly",start_date, start_date)
   filtered_hourly = filter_hourly_weather (hourly)
   current_weather = filtered_hourly[0]
   #print(hourly)
   daily = get_weather  (conn, "daily" , start_date,"2024-08-31" )
   filtered_weather_daily = filter_daily_weather(daily)
   #print (daily) 
   monthly= get_weather (conn, "monthly", "2024-01-01", "2024-12-31" )
   #print(monthly)
      
   return render(request, "home.html", {'current_weather' : current_weather , 'weather_hourly' :filtered_hourly   , 'weather_daily': filtered_weather_daily , 'weather_monthly':filter(filter_monthly_weather , monthly)})