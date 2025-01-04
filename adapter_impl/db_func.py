import os
from influxdb import InfluxDBClient

DATABASE = 'tema3'
db_client = InfluxDBClient('influxdb', 8086, None, None)

databases = db_client.get_list_database()
# create the db if it does not already exist
if not any(db['name'] == DATABASE for db in databases):
    db_client.create_database(DATABASE)

db_client.switch_database(DATABASE)

def save_to_db(payload):
    db_client.write_points(payload, time_precision='s')