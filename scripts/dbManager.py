# imports
import logging

from influxdb import InfluxDBClient

# configs
logging.basicConfig(level=logging.DEBUG)


class dbManager():
    def __init__(self, client=InfluxDBClient(host='localhost', port=8086, database="thiemo")):
        self.client = client

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
    def add_data_solar(self, db_name):
        self.client.write(['cpu,atag=test1 idle=20,usertime=10,system=1'], {'db': db_name}, 204, 'line')

    def read_data_from_solar(self, db_name="thiemo", device="cpu", measurement="*"):
        self.client.switch_database(db_name)
        results = self.client.query(("SELECT %s from %s ORDER by time DESC") % (measurement, device))
        points = results.get_points()

        list_items = []
        for item in points:
            list_items.append(item)

        return list_items


manager = dbManager()

print(manager.read_data_from_solar())
