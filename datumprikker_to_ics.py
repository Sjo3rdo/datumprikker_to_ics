from selenium import webdriver
import pandas as pd
import csv_ical
from datetime import datetime
from datetime import timedelta

url = "Put the URL from datumprikker.nl here"

def get_dates():
    """This function scrapes the dates from the website datumprikker.nl. It uses the Chromedriver.
    The result is stored in al list called dates. The dates are then written in a csv-file."""
    driver = webdriver.Chrome('Path where Chromedriver is installed')
    driver.get(url)
    
    #This line checks the webpage for any line that contains '2020-' OR '2021-'
    datums = driver.find_elements_by_xpath("//*[contains(@data-startdate,'2020-')] | //*[contains(@data-startdate,'2021-')]" )
    dates = []
    for i in (datums):
        dates.append(i.get_attribute('data-startdate'))
    
    f = open('dates.csv', 'w+')
    f.writelines("%s\n" % j for j in dates)
    
def dates_add_extra_info(dict_dates):
    """The created csv file is being read as a dataframe. A couple of columns are added so that we can use """
    df = pd.read_csv('The path to where the csv-file is saved')
    df['Event'] = 'Type here your event'
    df['Location'] = 'Type here your location'
    #The UTC part of the sting is being deleted here
    df['Date'] = test['Datum'].astype(str).str[:-6]
    # Date is put to datetime so that we can use timedelta on it
    df['Date'] = pd.to_datetime(test['Date'], yearfirst=True, utc=False)
    
    #I tried to make this a whole day event, but that didn't work yet. Any suggestions?
    df['End_date'] = test['Date'] + timedelta(days=1)
    #The Date and End_date column are being formatted to d-m-Y
    df['Date'] = test['Date'].dt.strftime('%d-%m-%Y')
    df['End_date'] = test['End_date'].dt.strftime('%d-%m-%Y')
    # The extra info is added to a new csv-file. This file will be used in the next function
    df.to_csv('data_datumprikker.csv')


def csv_to_ics():
    """This function is used from Github (https://github.com/albertyw/csv-ical). Credits to Albertyw"""
    convert = csv_ical.Convert()
    csv_file_location = 'location of the csv-file data_datumprikker.csv'
    ics_file_location = 'Location where you want your ics-file'

    csv_configs = {
        'HEADER_ROWS_TO_SKIP': 1,
        'CSV_NAME': 2,
        'CSV_START_DATE': 4,
        'CSV_END_DATE': 5,
        'CSV_DESCRIPTION': 2,
        'CSV_LOCATION': 3,
    }

    convert.read_csv(csv_file_location, csv_configs)

    i = 0
    while i < len(convert.csv_data):
        row = convert.csv_data[i]
        start_date = row[csv_configs['CSV_START_DATE']]
        end_date = row[csv_configs['CSV_END_DATE']]
        try:
            row[csv_configs['CSV_START_DATE']] = datetime.strptime(start_date, '%d-%m-%Y')
            row[csv_configs['CSV_END_DATE']] = datetime.strptime(end_date, '%d-%m-%Y')
            print(row)
            i += 1
        except ValueError:
            convert.csv_data.pop(i)
            print('pop')

    convert.make_ical(csv_configs)
    convert.save_ical(ics_file_location)
