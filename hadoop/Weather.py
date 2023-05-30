from mrjob.job import MRJob

class WeatherAnalysis(MRJob):
    
    def mapper(self, _, line):
        if not line.startswith("Date"):  # Skip the header line
            _, temperature, dew_point, wind_speed = line.strip().split(",")
            yield "Weather", (float(temperature), float(dew_point), float(wind_speed))
    
    def reducer(self, key, values):
        total_temperature = 0
        total_dew_point = 0
        total_wind_speed = 0
        count = 0
        
        for temperature, dew_point, wind_speed in values:
            total_temperature += temperature
            total_dew_point += dew_point
            total_wind_speed += wind_speed
            count += 1
        
        avg_temperature = total_temperature / count
        avg_dew_point = total_dew_point / count
        avg_wind_speed = total_wind_speed / count
        
        yield key, {
            'avg_temperature': avg_temperature,
            'avg_dew_point': avg_dew_point,
            'avg_wind_speed': avg_wind_speed
        }

if _name_ == '_main_':
    WeatherAnalysis.run()