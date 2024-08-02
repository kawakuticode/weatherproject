from django.db import models

'''
Create your models here.
Dew Point (DWPT): The temperature at which air becomes saturated with moisture and dew forms. It represents the point at which air reaches 100% relative humidity and condensation occurs1.
Relative Humidity (RH): The percentage of moisture in the air relative to the maximum amount the air can hold at a given temperature. It indicates how close the air is to saturation1.
Wind Speed (WSPD): The rate at which air moves horizontally. It’s usually measured in knots or miles per hour (mph)1.
Wind Direction (WDIR): The compass direction from which the wind is blowing. For example, a wind from the north has a wind direction of 360°1.
Pressure (PRES): Atmospheric pressure, typically measured in millibars (mb) or inches of mercury (inHg). It reflects the weight of the air above a location1.
Temperature (TEMP): The measure of heat energy in the air. It’s usually reported in degrees Celsius (°C) or Fahrenheit (°F)1.
Precipitation 
(PRCP): Any form of water—rain, snow, sleet, or hail—that falls from the atmosphere and reaches the ground1.
Snow: The amount of snowfall in inches or centimeters1.
Cloud Cover (COCO): A numerical value representing the extent of cloud cover, often on a scale from 0 to 8 (where 0 indicates clear skies and 8 indicates complete cloud cover).
'''
class Weather: 
    
    def __init__(self, interval) :
                 self.interval = interval
    
    def weather_customer_decoder(self):
        pass
       
    def __repr__(self) :
        pass
    
 
class Weather_hourly(Weather): 
    
    def __init__(self, time, temp,dwpt , rhum, prcp,snow, wdir , wspd , wpgt, pres,tsun, coco) :
        super().__init__("hourly")
        self.time = time
        self.temp = temp
        self.dwpt = dwpt
        self.rhum = rhum
        self.prcp = prcp
        self.snow = snow
        self.wdir = wdir
        self.wspd = wspd 
        self.wpgt = wpgt 
        self.pres = pres
        self.tsun = tsun
        self.coco = coco
                 
                 
    def get_wind_direction(self) : 
        direction:str = ""
        try : 
            directions = ['North',  'North-Northeast', 'Northeast', 'East-Northeast', 
                      'East','East-Southeast','Southeast' , 'South-Southeast','South'
                      'South-Southwest', 'Southwest', 'West-Southwest','West' 'West-Northwest', 
                      'Northwest', 'North-Northwest'] 
        
            index = round (self.wdir/22.5) % 16 
            '''print(self.wdir)
            print(index)
            print(len(directions))
            direction = directions[index]  '''
        except IndexError : 
            print("out of index")
        return direction
    
    def get_cloud_cover_info(self) : 
        
        cloud_status = { 0: 'Clear sky',1: 'Mostly Clear', 2: 'Partly cloudy', 3: 'Partly cloudy',
                         4: 'Partly to mostly cloudy',5: 'Mostly cloudy', 6: 'Mostly cloudy', 7: 'Very cloudy',
                         8:'Overcast'}
        return cloud_status.get(self.coco)
    
    def weather_custom_decoder(self): 
        return Weather_hourly(self['time'], self['temp'] ,self['dwpt'] , self['rhum'], self['prcp'], self['snow'], self['wdir'],
                           self['wspd'] ,self['wpgt'] ,self['pres'] ,self['tsun'] ,self['coco'])
    
    def __repr__(self) :
        return f"Weather_hourly( time = {self.time},temperature = {self.temp}, dewpoint = {self.dwpt}, relativehumidity = {self.rhum}, preciptation = {self.prcp} , snow = {self.snow}, winddirection = {self.get_wind_direction()}, wind_speed = {self.wspd} , wind_pgt = {self.wpgt } , pressure = {self.pres } , temperature_sun = {self.tsun } ,cloud_cover = {self.get_cloud_cover_info()})"          



#daily {'date': '2024-01-02', 'tavg': 8.6, 'tmin': 6.2, 'tmax': 11.0, 'prcp': 7.9, 'snow': 0.0, 'wdir': 208.0, 'wspd': 29.2, 'wpgt': 62.6, 'pres': 1000.3, 'tsun': 0}

class Weather_daily(Weather): 
    
    def __init__(self, date, tavg,tmin , tmax, prcp,snow, wdir, wspd , wpgt, pres,tsun) :
        super().__init__("daily")
        self.date = date
        self.tavg = tavg
        self.tmin = tmin
        self.tmax = tmax
        self.prcp = prcp
        self.snow = snow
        self.wdir = wdir
        self.wspd = wspd 
        self.wpgt = wpgt 
        self.pres = pres
        self.tsun = tsun
    
                 
                 
    def get_wind_direction(self) : 
        
        pass
    
    def get_cloud_cover_info(self) : 
        
        pass
    
    def weather_custom_decoder(self): 
        return Weather_daily(self['date'], self['tavg'] ,self['tmin'] , self['tmax'], self['prcp'], self['snow'], self['wdir'],
                           self['wspd'] ,self['wpgt'] ,self['pres'] ,self['tsun'])
    
    def __repr__(self) :
        return f"Weather_daily( date = {self.date},temperature average = {self.tavg}, temperature min = {self.tmin}, temperature max = {self.tmax}, preciptation = {self.prcp} , snow = {self.snow}, winddirection = {self.get_wind_direction()}, wind_speed = {self.wspd} , wind_pgt = {self.wpgt } , pressure = {self.pres } , temperature_sun = {self.tsun })"
     
    #montly 'date': '2024-02-01', 'tavg': 8.2, 'tmin': 4.4, 'tmax': 11.6, 'prcp': 83.4, 'wspd': 16.3, 'pres': 1014.8, 'tsun': 3683}
class Weather_monthly(Weather): 
    
    def __init__(self, date, tavg, tmin , tmax, prcp, wspd , pres,tsun) :
        super().__init__("monthly")
        self.date = date
        self.tavg = tavg
        self.tmin = tmin
        self.tmax = tmax
        self.prcp = prcp
        self.wspd = wspd
        self.pres = pres
        self.tsun = tsun
                 
                 
    def get_wind_direction(self) : 
        pass
    
    def get_cloud_cover_info(self) : 
        pass
    
    def weather_custom_decoder(self): 
        return Weather_monthly(self['date'], self['tavg'] ,self['tmin'] , self['tmax'], self['prcp'],
                           self['wspd'],self['pres'],self['tsun'])
    
    def __repr__(self) :
        return f"Weather_monthly( date = {self.date},temperature average = {self.tavg}, temperature min = {self.tmin}, temperature max = {self.tmax}, preciptation = {self.prcp} , wind_speed = {self.wspd} , pressure = {self.pres } , temperature_sun = {self.tsun })"
    
    