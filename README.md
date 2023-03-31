# Scrape time varying environmental data from a web site to generate time series of env. variables.

## Group Members
- Ashik Mahmud 27672 @ashik-devops [I'm an inline-style link](https://www.google.com)
- Ruhi Tamanna Alam 28370

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

For georeferencing five gauge locations, a set of location maps were downloaded from a provided URL and cropped to fit the image. The following process was then undertaken:

- Selected Georeferencer option from the Layers tab (For Mac)
- Opened the map using the "Open Raster" option
- Chose a suitable Ground Control Point (GCP) in the raster image through the "Add Point"(Yellow Button)
- Selected "From Map Canvas" option from the new pop-up window and chosen a reference point on openstreet map
- Clicked on the "Ok" button to add the GCP point entry for the raster image,gcp table and the map
- The process should be repeated till the image is well georeferenced. Then, some trnasformation setting "Thin Plain Spline" and the Target CRS to "EPSG:25832 - ETRS89 / UTM zone 32N" should be done from transformation/settings menu
- Upon pressing the play button in green, the georeferencer creates a layer with the rastered map on top of the openstreet map
### PostgreSQL / PostGIS:

The project employs a PostgreSQL database to store the extracted master data and periodic data. The database contains two main tables - "Masterdata" and "Waterlevel" - which store the respective data sets. The database also features geospatial extensions, such as PostGIS, to facilitate geospatial data processing.Then inside the database, these extensions should be created to enable postgis

                           brew install postgis (for windows Chocolatey)
                           -- Enable PostGIS (as of 3.0 contains just geometry/geography)
                           CREATE EXTENSION postgis;
                           -- enable raster support (for 3+)
                           CREATE EXTENSION postgis_raster;
                           -- Enable Topology
                           CREATE EXTENSION postgis_topology;
                           -- Enable PostGIS Advanced 3D
                           -- and other geoprocessing algorithms
                           -- sfcgal not available with all distributions
                           CREATE EXTENSION postgis_sfcgal;
                           -- fuzzy matching needed for Tiger
                           CREATE EXTENSION fuzzystrmatch;
                           -- rule based standardizer
                           CREATE EXTENSION address_standardizer;
                           -- example rule data set
                           CREATE EXTENSION address_standardizer_data_us;
                           -- Enable US Tiger Geocoder
                           CREATE EXTENSION postgis_tiger_geocoder;



The finalScript.sql file is used for running neccessary sql commands to created role, database and necessary table. This file can be separated into multiple files to execute with psql or can be used by commenting out all other segments except one.

### Periodic Data Scrapper:

The periodic data scrapper is a Python script that extracts water level and discharge data at regular intervals. It uses BeautifulSoup for web scraping and stores the extracted data in a PostgreSQL table named "Waterlevel". This script is set up as a cron job along with insertData script to ensure regular updates and maintain the current status of the database using this shell script

                                          cd /Users/name/yourpath
                                          while true; do
                                           python periodicScrapper.py && python insertData.py
                                           sleep 1000
                                          done 

- Get HTML content and parse with BeautifulSoup

                            base_url = 'https://howis.eglv.de/pegel/html/uebersicht_internet.php'
                            res = requests.get(base_url)
                            soup = BeautifulSoup(res.content, 'html.parser')

- Extract water level data from HTML and create station_data list

                          tooltips = soup.select('div.tooltip')
                          tooltip_data = []
                          headers = ['sid', 'pegelnummer','place', 'timestamp', 'water_level', 'discharge']
                          for i, div in enumerate(tooltips):
                          header = re.sub(r'\s+', ' ', div.select_one('.tooltip-head').text).strip()
                          values = div.select('td.tooltip-value')
                          station_data = [f's{i+1}', header, datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + [value.text.replace('\xa0', '').strip()                                 for value in values]
                          tooltip_data.append(station_data)

- Write station_data to CSV file
                          output = '/Users/ashikmahmud/MyDocuments/Personal/GEO2023EX/Final/output.csv'
                          if_file_exists = os.path.isfile(output)
                          for item in tooltip_data:
                              address_parts = item[1].split(' ')
                              item[1:2] = [address_parts[0], ' '.join(address_parts[1:])]
                          with open(output, 'w', newline='') as csvfile:
                              writer = csv.writer(csvfile)
                              writer.writerow(headers)
                              writer.writerows(tooltip_data)

- Read CSV file and write to PostgreSQL database
                          engine_connect = sqlalchemy.create_engine("postgresql://env_master:M123xyz@localhost:5433/env_groundwater").connect()
                          df = pd.read_csv(output)
                          with engine_connect as connect:
                              df.to_sql('Waterlevel', con=connect, if_exists='append', index=False)

- Remove CSV file
                          os.remove(output)


### Master Data Scraper:

The master data scrapper is a Python script that utilizes the BeautifulSoup library to extract master data of gauges, including station identifiers, coordinates, and other essential parameters. This data is collected once and stored in a PostgreSQL table named "Masterdata".

Example URLs:
https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal=32
https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal=28

- Import packages: The script begins by importing necessary libraries and packages, such as requests, BeautifulSoup, geopandas, pandas, psycopg2, and sqlalchemy
- Create a connection to the database: It creates an engine using sqlalchemy.create_engine and connects to the PostgreSQL database named env_groundwater
- Scrape data from the website
all_stm_url = r"https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal="
base_url="https://howis.eglv.de/pegel"

                   consolidated_array=[]
                   def download_image(url, file_path):
                       ... function to download image and save it to a local file

                   for i in range(1, 100):
                       url = all_stm_url + str(i)
                       res = requests.get(url)
                       soup = BeautifulSoup(res.content, 'html.parser')
                       stammDaten = soup.select_one('#popupcontenttitle').text.strip().split(':')[1].strip()
                       div_tag = soup.find('div', {'id': 'mapcontainer'})
                       local_file_path = None
                       if div_tag:
                           img_tag = div_tag.find('img', {'border': '0'})
                           if img_tag:
                               ...download the image

                           else:
                               print("Image tag not found.")
                       else:
                           print("Div tag not found.")
                       ... extract the data from the HTML

                       consolidated_array.append(pairs)

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
 - Filtering and transforming the Data
                   data_filtered = [d for d in consolidated_array if not all(v == "-" for v in d.values())]

                   for d in data_filtered:
                       for k, v in d.items():
                           if v == '' or v == '-':
                               d[k] = None
                               
 - Create a GeoDataFrame from the cleaned data and save it to a GeoPackage file
                         df = pd.DataFrame(data_filtered)
                         df_cleaned = df[df['Rechtswert'].notnull()]
                         gdf = gpd.GeoDataFrame(df_cleaned, geometry=gpd.points_from_xy(df_cleaned.Rechtswert, df_cleaned.Hochwert), crs="EPSG:31466")
                         gdf.to_file("GW_Stations.gpkg", layer='GW Stations', driver="GPKG")

 - Save the data to a PostgreSQL database
                         gdf.to_postgis(con=engine, name="Masterdata", schema="public", index=True, chunksize=100, if_exists="replace")
 
 The script outputs the following:

 A GeoPackage file named "GW_Stations.gpkg", containing the GeoDataFrame with the station data
 A PostgreSQL database named "env_groundwater" with a table named "Masterdata" containing the station data


### Image Data

For the images in master data website, we can store it as a BLOB in the PostgreSQL database. However, it might be more convenient to store the images on disk and reference their file paths in the database. Thats what has exactly been done, the absolute filepath is saved in the database and the images are saved in the created relative directory images.

                            def download_image(url, file_path):
                                response = requests.get(url, stream=True)
                                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                                with open(file_path, 'wb') as f:
                                    for chunk in response.iter_content(chunk_size=8192):
                                        f.write(chunk)

### QGIS Temporal Controller 

QGIS, an open-source GIS software, is used to visualize the data in a geospatial context. The temporal controller feature in QGIS allows generating time-lapse visualizations of the data, which can help identify patterns and trends in the water resource system.

- Create two separate layers, one for the water level table without geometry and the other for the master data with geometry.
- Open the toolbox and select "join by value."
- Input the intended field to join and selected the join type as "one to many," then run the process.
- The merged data should be visible in a joined layer attribute table.
- Enabled the temporal controller with timestamp from the layer properties.
 -Used the symbology as graduated with appropriate classification and equal interval.
- Selected the clock icon from the toolbar to pop up the temporal controller, then play the animation. This should display the water level changes over time.

