import mysql.connector

def create_connection():
    try:
        cnx = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="acme_homeowners_insurance"
        )
        return cnx
    except mysql.connector.Error as err:
        print("Error creating connection:", err)
        return None

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
