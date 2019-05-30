import mysql.connector as mariadb


class DataHandler:
    def __init__(self, database, user, password):
        self.conn = mariadb.connect(database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def save_data(self, sensor, data):
        try:
            self.cursor.execute("INSERT INTO data (sensor, value) VALUES (%s, %s)", (sensor, data))
            self.conn.commit()
            print("Saved sensor {}={} to database".format(data, sensor))
            return True
        except Exception as e:
            print("DB update failed: {!s}".format(e))
            return False

'''
#sensors

tb = temp bed
th = temp hotend
ta = temp ambient
tf = temp fillament

hp = humidity printer
hf = humidity filament

co = co2
tv = tvoc
'''