import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "myAdmin",
        password = "tfr-Rms@2025",
        database = "blue_ocean_bar_db"
    ) 

