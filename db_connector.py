import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host = "192.168.137.250",
        user = "myAdmin",
        password = "tfr-Rms@2025",
        database = "blue_ocean_bar_db"
    ) 

