# https://www.youtube.com/watch?v=49hKs_H5Xf0&t=25s&ab_channel=DevOpsJourney
from influxdb import InfluxDBClient

#Setup database
db_client = InfluxDBClient('localhost', 8086, None, None)

# Check if the database exists and create it if necessary
databases = db_client.get_list_database()
if not any(db['name'] == 'mydb' for db in databases):
    db_client.create_database('mydb')

db_client.switch_database('mydb')

def save_to_db(payload):
    print("Payload will be saved to db: ", payload)
    db_client.write_points(payload, time_precision='s')
    print("Saved to db!")
