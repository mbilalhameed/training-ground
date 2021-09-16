import csv
import glob
import os

from datetime import datetime

class Reader:
    
    list_of_files = []
    weather_readings = {}

    def ignore_empty_values(self, weather_reading):
        refactored_weather_reading = {}
        for key, value in weather_reading.items():
            if value:
                if value and '.' not in value:
                    refactored_weather_reading[key] = int(value)
                else:
                    refactored_weather_reading[key] = float(value)
            else:
                return None
        return refactored_weather_reading


    def read_data(self):
        """Reads data files and populates a nested dictionary to store data

        Args:
            path_to_files ([String]): [path to directory containing data files]
        """
        required_keys = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity', ' Min Humidity']
        for file_name in self.list_of_files:
            with open(file_name, mode='r') as csv_file:
                for single_day_weather_reading in csv.DictReader(csv_file):
                    if single_day_weather_reading:
                        
                        if single_day_weather_reading.get('PKT'):
                            date = datetime.strptime(str(single_day_weather_reading['PKT']), "%Y-%m-%d")
                        else:
                            date = datetime.strptime(str(single_day_weather_reading['PKST']), "%Y-%m-%d")
                        weather_reading = {required_key:single_day_weather_reading[required_key]
                                    for required_key in required_keys if required_key in single_day_weather_reading}
                        
                        refactored_weather_reading = self.ignore_empty_values(weather_reading)
                        if refactored_weather_reading is not None:
                            refactored_weather_reading['date'] = date
                            self.weather_readings.setdefault(date.year, {}).setdefault(date.month, []).append(refactored_weather_reading)
        return self.weather_readings


    def compile_list_of_files(self, date, path_to_files):
        self.list_of_files = []
        self.weather_readings = {}
        date = date.split('/')
        
        if len(date) == 1:
            year = date[0]
            month = ""
        else:
            year = date[0]
            month = datetime.strptime(date[1],"%m").strftime("%b")
            
        for file_name in glob.glob(os.path.join(path_to_files, '*.txt')):
            if year in file_name and month in file_name:
                self.list_of_files.append(file_name)
