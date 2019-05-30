import mysql.connector as mariadb

conn = mariadb.connect(database='site', user='mct', password='mct')
cursor = conn.cursor()


try:
    cursor.execute("INSERT INTO printer (idprinter, printer_name, printer_owner) VALUES (1, 'Ender x-3000', 'arno')")
    conn.commit()
    print("succsess")
except Exception as e:
    print("DB update failed: {!s}".format(e))