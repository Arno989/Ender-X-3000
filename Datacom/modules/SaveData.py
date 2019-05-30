import mysql.connector as mariadb


class DataHandler:
    def __init__(self, database, user, password):
        self.conn = mariadb.connect(database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def save_data(self, sensor, data):
        try:
            self.cursor.execute("INSERT INTO data (sensor, value) VALUES (%s, %s)", (sensor, data))
            self.conn.commit()
            print("Saved sensor '{}' with value '{}' to database".format(sensor, data))
            return True
        except Exception as e:
            print("DB update failed: {!s}".format(e))
            return False
