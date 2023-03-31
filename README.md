# Title: Scraping Environmental Data and Visualizing in QGIS

## Introduction

The goal of this assignment is to collect, georeference, process, and store time-varying environmental data from a website in order to generate a time series of environmental variables. The primary goal is to build a comprehensive database that contains gauge master data as well as periodic water level and discharge data. This information is crucial for understanding, monitoring, and managing water resources and can be used for various purposes, such as flood prediction, water supply management, and environmental impact assessments.

The data is scraped from the Water Boards Emschergenossenschaft und Lippeverband website, which provides up-to-date information on water levels, discharges, and other related environmental parameters. The assignment is divided into multiple parts, including the scrapping of a master data set, a periodic data set, and the insertion of the scraped data in the PostgreSQL database after the creation of necessary PostgreSQL database tables to store the information.

The master data scraper is in charge of obtaining gauge master data, such as station identifiers, coordinates, and other critical parameters. This data is collected once and stored in a PostgreSQL table named "Masterdata." On the other hand, the periodic data scraper focuses on extracting water level and discharge data at regular intervals. This data is stored in a PostgreSQL table named "Waterlevel." The periodic data scraper is configured as a cron job, ensuring that the data is updated on a regular basis and the database is kept up to date.

The assignment also involves georeferencing five gauge location pictures on the maps and linking them to the database. By creating time-lapse visualizations of the data using the temporal controller feature in QGIS, it is possible to spot patterns and trends in the system of water resources.

In conclusion, this assignment demonstrates a thorough method for gathering and managing environmental data, offering helpful insights for managing and making decisions about water resources. The data collected can be used to develop predictive models, inform policy decisions, and contribute to a better understanding of water resource systems.

## Installations
 - QGIS
 - Anaconda
 - Postgresql and Postgis
 - Necessary packages after configuring the environment like sqlalchemy psycopg2 pgspecial ipython-sql jupyterlab geopandas etc.

## Objective

The main objectives of this assignment are:

- Georeference gauge location maps.
- Create a PostgreSQL schema, tables, and views
- Scrape time series data of water discharge and water level from the website.
- Scrape master data of gauges from the website and store it in a PostgreSQL table.
- Visualize the data using QGIS and create a dynamic map with the temporal controller.



## Methodology

### Georeference Gauge Location Maps:

We will georeference the gauge location maps provided by the website.
Example image: https://howis.eglv.de/pegel/images/stationpics/maps/20012_stadtplan.gif

### PostgreSQL / PostGIS:

The project employs a PostgreSQL database to store the extracted master data and periodic data. The database contains two main tables - "Masterdata" and "Waterlevel" - which store the respective data sets. The database also features geospatial extensions, such as PostGIS, to facilitate geospatial data processing.

### Periodic Data Scrapper:

The periodic data scrapper is another Python script that extracts water level and discharge data at regular intervals. It uses BeautifulSoup for web scraping and stores the extracted data in a PostgreSQL table named "Waterlevel". This script is set up as a cron job to ensure regular updates and maintain the current status of the database.

### Master Data Scraper:

The master data scrapper is a Python script that utilizes the BeautifulSoup library to extract master data of gauges, including station identifiers, coordinates, and other essential parameters. This data is collected once and stored in a PostgreSQL table named "Masterdata".

Example URLs:
https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal=32
https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal=28

- Import packages: The script begins by importing necessary libraries and packages, such as requests, BeautifulSoup, geopandas, pandas, psycopg2, and sqlalchemy
- Create a connection to the database: It creates an engine using sqlalchemy.create_engine and connects to the PostgreSQL database named env_groundwater
- Create a function to create key-value pairs: A function named create_key_value_pairs is defined to parse the labels and values from the scraped HTML and create a dictionary of key-value pairs
                  def create_key_value_pairs(labels_values):
                      result = {}
                      current_label = None

                      for item in labels_values:
                          if ":" in item:
                              current_label = item.replace(":", "")
                              result[current_label] = None
                          elif current_label is not None:
                              result[current_label] = item

                      return result


### Image Data

For the image in master data website, we can store it as a BLOB in the PostgreSQL database. However, it might be more convenient to store the images on disk and reference their file paths in the database. Thats what has exactly been done, the absolute filepath is saved in the database and the image is saved in the relative directory images.

### QGIS Temporal Controller 

QGIS, an open-source GIS software, is used to visualize the data in a geospatial context. The temporal controller feature in QGIS allows generating time-lapse visualizations of the data, which can help identify patterns and trends in the water resource system.

