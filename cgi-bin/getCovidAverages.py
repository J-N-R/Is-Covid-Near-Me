#!/usr/local/bin/python3.8
#
# getCovidAverages.py
#
# Description:
#    Python CGI program that recieves a state and county and
#    returns their current covid information in JSON format.
#
#    To be used by "Is Covid Near Me?"
#
# Made by rivejona@kean.edu
#

import cgi
import sys
import cgitb
from datetime import date, timedelta
import pandas as pd

print('Content-Type: application/json\n')

# Create and initialize CGI Variables
cgitb.enable()
form = cgi.FieldStorage()
state  = form.getvalue('state').lower()
county = form.getvalue('county').lower()

# If no parameters passed, kill early
if 'state' not in form or 'county' not in form:
  print('{"error": "No Params Given"}')
  sys.exit()

# Load data into dataframe
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties-recent.csv'
df = pd.read_csv(url, usecols = ['date', 'county', 'state', 'cases', 'cases_avg', 'deaths', 'deaths_avg'], index_col=False, error_bad_lines=False)

# Attempt to select specific record
yesterday = date.today() - timedelta(days=1)
result = df.loc[(df['state'].str.lower() == state) & (df['county'].str.lower() == county) & (df['date'] == str(yesterday))]

# If record doesn't exist, kill early, otherwise print data
if result.empty:
  print('{"error": "Not Found"}')
else:
  result.fillna(0)
  result = result[['cases', 'cases_avg', 'deaths', 'deaths_avg', 'state', 'county']]
  result.rename(columns={"cases": "newCases", "cases_avg": "avgCases", "deaths": "newDeaths", "deaths_avg": "avgDeaths"}, inplace=True)
  print(result.to_json(orient='records')[1:-1])