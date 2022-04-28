import argparse
import re
import os

from calculations.temperature_calculations import TemperatureCalculator
from files_reader.read_files import Reader
from reports.report_generator import ReportGenerator

class Driver:

    def is_valid_year(self, year):
        valid_year = re.compile(r'\b(200[4-9]|201[0-6])\b')
        
        if valid_year.search(year):
            return year
        else:
            raise argparse.ArgumentTypeError(f"Invalid year {year} should be between 2004-2016")

        
    def is_valid_month(self, month):
        if 1 <= int(month) <= 12:
            return month
        else:
            raise argparse.ArgumentTypeError(f"Invalid month {month}")

    
    def is_valid_date(self, date):
        year = date.split('/')[0]
        month = date.split('/')[1]
        
        self.is_valid_year(year)
        self.is_valid_month(month)
        
        return date
            

    def is_valid_directory_path(self, directory_path):
        if os.path.isdir(directory_path):
            return directory_path
        else:
            raise argparse.ArgumentTypeError(f"{directory_path} is not a valid path")


    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Analyze weather man data')
        
        parser.add_argument(
            '-path', 
            help='Path to folder containing data files', 
            type=self.is_valid_directory_path, 
            required=True
        )
        parser.add_argument('-a', help='Year and month as yyyy/m', type=self.is_valid_date)
        parser.add_argument('-c', help='Year and month as yyyy/mm', type=self.is_valid_date)
        parser.add_argument('-e', help='Year as yyyy', type=self.is_valid_year)
        
        return parser.parse_args()


    def run_weather_man(self):
        files_reader = Reader()
        generate_report = ReportGenerator()
        calculate_temperature = TemperatureCalculator()
        parsed_arguments = self.parse_arguments()
        arguments = vars(parsed_arguments)
        
        if arguments['e']:
            files_reader.compile_list_of_files(arguments['e'], arguments['path'])
            complete_weather_data = files_reader.read_weather_data()
            yearly_weather_readings = calculate_temperature.compile_data_for_yearly_calculations(
                complete_weather_data
            )
            calculate_temperature.highest_lowest_temperature(
                yearly_weather_readings, arguments['e']
            )
            
        if arguments['a']:
            files_reader.compile_list_of_files(arguments['a'], arguments['path'])
            complete_weather_data = files_reader.read_weather_data()
            monthly_weather_readings = calculate_temperature.compile_data_for_monthly_calculations(
                complete_weather_data
            )
            calculate_temperature.average_highest_lowest_temperature(
                monthly_weather_readings, arguments['a']
            )
            
        if arguments['c']:
            files_reader.compile_list_of_files(arguments['c'], arguments['path'])
            complete_weather_data = files_reader.read_weather_data()
            monthly_report_readings = generate_report.compile_data_for_monthly_reports(
                arguments['c'], complete_weather_data
            )
            generate_report.bar_charts_for_temperature(monthly_report_readings)
            generate_report.single_bar_chart_temperature(monthly_report_readings)


def main():
    driver = Driver()
    driver.run_weather_man()


if __name__ == "__main__":
    main()
