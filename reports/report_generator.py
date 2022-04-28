class ReportGenerator:
    
    def compile_data_for_monthly_reports(self, date, weather_readings):
        maximum_temperature = {}
        minimum_temperature = {}
        
        for key_year, year in weather_readings.items():
            for key_month, month in year.items():
                
                maximum_temperature.setdefault(key_year, {}).setdefault(
                    key_month, [daily_readings['Max TemperatureC'] 
                    for daily_readings in month]
                )
                minimum_temperature.setdefault(key_year, {}).setdefault(
                    key_month, [daily_readings['Min TemperatureC'] 
                    for daily_readings in month]
                )
                    
        date = date.split('/')
        year = int(date[0])
        month = int(date[1])
        
        yearly_maximum_reading = maximum_temperature[year]
        yearly_minimum_reading = minimum_temperature[year]
        
        return {
            'yearly_maximum_temperature': yearly_maximum_reading[month],
            'yearly_minimum_temperature': yearly_minimum_reading[month]
        }
    
    
    def bar_charts_for_temperature(self, weather_readings):
        """generates a bar chart of maximum and minimum temperature on each day of a month

        Args:
            weather_readings ([List]): [Nested list of given month data]
        """
        CRED = '\33[31m'
        CBLUE = '\33[34m'
        CWHITE = '\33[37m'
        
        min_temperature = weather_readings['yearly_minimum_temperature']
        max_temperature = weather_readings['yearly_maximum_temperature']
        
        for day, weather_reading in enumerate(weather_readings['yearly_maximum_temperature']):
            print(f"{day+1} {CRED}", '+' * int(max_temperature[day]), f"{CWHITE} {max_temperature[day]}C")
            print(f"{day+1} {CBLUE}", '+' * int(min_temperature[day]), f"{CWHITE} {min_temperature[day]}C")


    def single_bar_chart_temperature(self, weather_readings):
        """generates a bar chart of maximum and minimum temperature on each day of a month

        Args:
            weather_readings ([List]): [Nested list of given month data]
        """
        CRED = '\33[31m'
        CBLUE = '\33[34m'
        CWHITE = '\33[37m'
        
        min_temperature = weather_readings['yearly_minimum_temperature']
        max_temperature = weather_readings['yearly_maximum_temperature']
        
        for day, weather_reading in enumerate(weather_readings['yearly_maximum_temperature']):
            print(
                day+1, 
                CBLUE + "+"*int(min_temperature[day]) 
                + CRED + "+"*int(max_temperature[day]) 
                + CWHITE, min_temperature[day], "-", max_temperature[day]
            )
