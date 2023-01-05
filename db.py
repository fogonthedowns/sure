import mysql.connector
import os

host = os.getenv("MYSQL_HOST", "localhost")
password = os.getenv("MYSQL_PASSWORD", "")
user = os.getenv("MYSQL_USER", "root")


def create_connection():

    connection = mysql.connector.connect(
        host=host,
        password=password,
        user=user
    )
    cursor = connection.cursor()

    # Create the database if it does not exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS acme_homeowners_insurance")
    connection.commit()

    # Connect to the database
    connection = mysql.connector.connect(
        host=host,
        password=password,
        user=user,
        database="acme_homeowners_insurance"
    )

    return connection


def create_table(cnx):
    try:
        cursor = cnx.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                uuid CHAR(36) NOT NULL,
                name VARCHAR(255) NOT NULL,
                coverage_type VARCHAR(255) NOT NULL,
                state VARCHAR(255) NOT NULL,
                has_pet BOOLEAN NOT NULL,
                flood_coverage BOOLEAN NOT NULL
            )
        """
        cursor.execute(sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error creating table:", err)


def create_rate_table(cnx):
    try:
        cursor = cnx.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS rates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                state CHAR(2) NOT NULL,
                state_tax_percent DECIMAL(4, 4) NOT NULL,
                flood_percent DECIMAL(4, 4) NOT NULL,
                default_rate DECIMAL(10,2) NOT NULL,
                premium_rate DECIMAL(10,2) NOT NULL,
                pet_rate DECIMAL(10,2) NOT NULL
                
            )
        """
        cursor.execute(sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error creating rate table:", err)


def insert_initial_data(cnx):
    cursor = cnx.cursor()

    # magic numbers
    BASIC_RATE = 20
    PET_PREMIUM = 20
    PREMIUM_RATE = 40
    CA_TAX = 0.01
    CA_FLOOD = 0.02
    TX_TAX = 0.005
    TX_FLOOD = 0.5
    NY_TAX = 0.02
    NY_FLOOD = 0.1

    try:
        rates_data = [
            ("CA", CA_TAX, CA_FLOOD, BASIC_RATE, PREMIUM_RATE, PET_PREMIUM),
            ("TX", TX_TAX, TX_FLOOD, BASIC_RATE, PREMIUM_RATE, PET_PREMIUM),
            ("NY", NY_TAX, NY_FLOOD, BASIC_RATE, PREMIUM_RATE, PET_PREMIUM),
        ]

        insert_query = "INSERT INTO rates (state, state_tax_percent, flood_percent, default_rate, premium_rate, pet_rate) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, rates_data)

        cnx.commit()
    except Exception as e:
        print("Error inserting initial data: {}".format(e))
        cnx.rollback()


def delete_all_rates(cnx):
    cursor = cnx.cursor()
    sql = "TRUNCATE TABLE rates"
    try:
        cursor.execute(sql)
        cnx.commit()
    except Exception as e:
        print("Error deleting all rates: {}".format(e))
        cnx.rollback()
