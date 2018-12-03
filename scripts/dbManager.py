# imports
import logging

from influxdb import InfluxDBClient

from scripts.db_config import *

# configs
logging.basicConfig(level=logging.DEBUG, filename="log_db.txt")


class dbManager():
    def __init__(self, client=InfluxDBClient(host=HOST, port=PORT, database=DB_NAME)):
        self.client = client
        self.create_database(DB_NAME)

    # returns a list of all databases
    def get_all_databases(self):
        return self.client.get_list_database()

    # create database if it not yet exists
    def create_database(self, db_name):
        logging.debug("trying to create db: {0}".format(db_name))
        create = True

        databases = self.get_all_databases()
        for database in databases:
            if database["name"] == db_name:
                create = False
                logging.warning("database: {0} already exists".format(db_name))

        if create == True:
            logging.debug("creating database: {0}".format(db_name))
            self.client.create_database(dbname=db_name)

    # works but parameters for the db collumns need to be changed to something usefull
    def add_data_solar(self, pannel_voltage, battery_voltage, db_name="solar"):
        self.client.write(
            ['setup1,pannel_voltage={0} battery_voltage={1}'.format(str(pannel_voltage), str(battery_voltage))],
            {'db': db_name}, 204, 'line')

    def read_data_from_solar(self, device="setup1", measurement="*", amount=10000):
        results = self.client.query(("SELECT %s from %s ORDER by time DESC LIMIT  %s") % (measurement, device, amount))
        points = results.get_points()

        list_items = []
        for item in points:
            list_items.append(item)

        return list_items


db = dbManager()

db.add_data_solar(19.1, 12.1)
print(db.read_data_from_solar())
