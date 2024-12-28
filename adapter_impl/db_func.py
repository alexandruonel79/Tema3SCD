# https://www.youtube.com/watch?v=49hKs_H5Xf0&t=25s&ab_channel=DevOpsJourney
import os
from influxdb import InfluxDBClient

DATABASE = 'tema3'
#Setup database
db_client = InfluxDBClient('influxdb', 8086, None, None)

# Check if the database exists and create it if necessary
databases = db_client.get_list_database()
if not any(db['name'] == DATABASE for db in databases):
    db_client.create_database(DATABASE)

db_client.switch_database(DATABASE)

def save_to_db(payload):
    # print("Payload will be saved to db: ", payload)
    db_client.write_points(payload, time_precision='s')
    print("Saved to db!")
