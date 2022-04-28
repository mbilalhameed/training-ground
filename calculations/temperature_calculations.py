class TemperatureCalculator:
    
    def compile_data_for_yearly_calculations(self, weather_readings):
        minimum_temperature_every_month = {}
        maximum_temperature_every_month = {}
        maximum_humidity_every_month = {}
        
        for year_number, year_values in weather_readings.items():
            minimum_temperature = []
            maximum_temperature = []
            maximum_humidity = []
            
            for month_name, month_values in year_values.items():
                minimum_temperature.append(
                    min(month_values, key=lambda x: x['Min TemperatureC'])
                )
                minimum_temperature_every_month[year_number] = minimum_temperature
                
                maximum_temperature.append(
                    max(month_values, key=lambda x: x['Max TemperatureC'])
                )
                maximum_temperature_every_month[year_number] = maximum_temperature
                
                maximum_humidity.append(
                    max(month_values, key=lambda x: x[' Mean Humidity'])
                )
                maximum_humidity_every_month[year_number] = maximum_humidity
                
        return {
            'minimum_temperature_every_month': minimum_temperature_every_month, 
            'maximum_temperature_every_month': maximum_temperature_every_month, 
            'maximum_humidity_every_month': maximum_humidity_every_month
        }


    def compute_mean(self, column_key, month_values):
        sum_of_values = sum(daily_readings[column_key] for daily_readings in month_values)
        
        return float(sum_of_values//len(month_values))


    def compile_data_for_monthly_calculations(self, weather_readings):
        avg_minimum_temperature_every_month = {}
        avg_maximum_temperature_every_month = {}
        avg_mean_humidity_every_month = {}
        
        for key_year, year in weather_readings.items():
            for month_name, month_values in year.items():
                
                avg_maximum_temperature_every_month.setdefault(key_year, {}).setdefault(
                    month_name, self.compute_mean('Max TemperatureC', month_values)
                )
                
                avg_minimum_temperature_every_month.setdefault(key_year, {}).setdefault(
                    month_name, self.compute_mean('Min TemperatureC', month_values)
                )
                
                avg_mean_humidity_every_month.setdefault(key_year, {}).setdefault(
                    month_name, self.compute_mean(' Mean Humidity', month_values)
                )

        return {
            'avg_maximum_temperature_every_month': avg_maximum_temperature_every_month, 
            'avg_minimum_temperature_every_month': avg_minimum_temperature_every_month, 
            'avg_mean_humidity_every_month': avg_mean_humidity_every_month
        }


    def get_maximum_humidity_yearly(self, maximum_humidity_every_month):
        yearly_values = {}
        
        for key_date, monthwise_readings in maximum_humidity_every_month.items():
            yearly_values[key_date] = max(monthwise_readings, key=lambda x: x['Max Humidity'])
            
        return yearly_values


    def get_maximum_temperature_yearly(self, maximum_temperature_every_month):
        yearly_values = {}
        
        for key_date, monthwise_readings in maximum_temperature_every_month.items():
            yearly_values[key_date] = max(monthwise_readings, key=lambda x: x['Max TemperatureC'])
            
        return yearly_values


    def get_minimum_temperature_yearly(self, minimum_temperature_every_month):
        yearly_values = {}
        
        for key_date, monthwise_readings in minimum_temperature_every_month.items():
            yearly_values[key_date] = min(monthwise_readings, key=lambda x: x['Min TemperatureC'])
            
        return yearly_values


    def highest_lowest_temperature(self, yearly_weather_readings, year):
        """looks for highest temperature/humidity in a given year and month

        Args:
            yearly_weather_readings ([Dictionary]): [A nested dictionary containing all data]
            year ([String]): [Year given by user]
        """
        minimum_temperature_yearly = self.get_minimum_temperature_yearly(
            yearly_weather_readings['minimum_temperature_every_month']
        )[int(year)]
        maximum_temperature_yearly = self.get_maximum_temperature_yearly(
            yearly_weather_readings['maximum_temperature_every_month']
        )[int(year)]
        maximum_humidity_yearly = self.get_maximum_humidity_yearly(
            yearly_weather_readings['maximum_humidity_every_month']
        )[int(year)]
        
        maximum_temperature_date = maximum_temperature_yearly['date'].strftime("%d %b")
        minimum_temperature_date = minimum_temperature_yearly['date'].strftime("%d %b")
        maximum_humidity_date = maximum_humidity_yearly['date'].strftime("%d %b")
        
        print(f"Max Temperature {maximum_temperature_yearly['Max TemperatureC']} on {maximum_temperature_date}")
        print(f"Min Temperature {minimum_temperature_yearly['Min TemperatureC']} on {minimum_temperature_date}")
        print(f"Max Humidity {maximum_humidity_yearly['Max Humidity']} on {maximum_humidity_date}")


    def average_highest_lowest_temperature(self, monthly_weather_readings, date):
        """looks for highest temperature/humidity and lowest temperature given a particular year

        Args:
            monthly_weather_readings ([Dictionary]): [A nested dictionary containing all data]
            date ([Dictionary]): [A dictionary of given year, month and day]
        """
        year = int(date.split('/')[0])
        month = int(date.split('/')[1])
        
        print(f"Avg Max Temperature {monthly_weather_readings['avg_maximum_temperature_every_month'][year][month]}")
        print(f"Avg Min Temperature {monthly_weather_readings['avg_minimum_temperature_every_month'][year][month]}")
        print(f"Avg Mean Humidity {monthly_weather_readings['avg_mean_humidity_every_month'][year][month]}")
