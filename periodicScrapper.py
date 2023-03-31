#!/usr/bin/env python
# coding: utf-8

# ## Periodic data Scrapper

# In[5]:


from bs4 import BeautifulSoup
from shapely.geometry import Polygon
import geopandas as gpd
import os
import psycopg2
import sqlalchemy
from tabulate import tabulate
import csv
import requests
import re
from datetime import datetime

base_url = 'https://howis.eglv.de/pegel/html/uebersicht_internet.php'
res = requests.get(base_url)
soup = BeautifulSoup(res.content, 'html.parser')

tooltips = soup.select('div.tooltip')
tooltip_data = []

# Define headers
headers = ['sid', 'pegelnummer','place', 'timestamp', 'water_level', 'discharge']

# Loop through tooltip data and extract values
for i, div in enumerate(tooltips):
    header = re.sub(r'\s+', ' ', div.select_one('.tooltip-head').text).strip()
    values = div.select('td.tooltip-value')
    station_data = [f's{i+1}', header, datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + [value.text.replace('\xa0', '').strip() for value in values]
    tooltip_data.append(station_data)
    tooltip_data
output = '/Users/ashikmahmud/MyDocuments/Personal/GEO2023EX/Final/output.csv'
if_file_exists = os.path.isfile(output)
for item in tooltip_data:
    address_parts = item[1].split(' ')
    item[1:2] = [address_parts[0], ' '.join(address_parts[1:])]
    
print(tooltip_data)

# Write data to CSV file
with open(output, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(tooltip_data)


# In[6]:




