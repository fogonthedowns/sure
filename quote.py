import uuid
from db import create_connection, create_table

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

class Quote:
    def __init__(self, name, coverage_type, state, has_pet, flood_coverage):
        required_attributes = [
            ("name", name),
            ("coverage_type", coverage_type),
            ("state", state),
            ("has_pet", has_pet),
            ("flood_coverage", flood_coverage)
        ]
        for attr_name, attr_value in required_attributes:
            if attr_value is None:
                raise ValueError("'{}' is a required attribute for Quote".format(attr_name))

        self.uuid = uuid.uuid4()
        self.name = name
        self.coverage_type = coverage_type
        self.state = state
        self.has_pet = has_pet
        self.flood_coverage = flood_coverage

    def save(self):
        connection = create_connection()
        cursor = connection.cursor()

        sql = "INSERT INTO quotes (uuid, name, coverage_type, state, has_pet, flood_coverage) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (str(self.uuid), self.name, self.coverage_type, self.state, self.has_pet, self.flood_coverage)
        try:
            cursor.execute(sql, values)
        except Exception as e:
            print("Error saving quote: {}".format(e))
            return

        connection.commit()
        connection.close()

        return str(self.id)

    @classmethod
    def get_by_uuid(cls, uuid):
        connection = create_connection()
        cursor = connection.cursor()

        sql = "SELECT * FROM quotes WHERE uuid=%s"
        try:
            cursor.execute(sql, (uuid,))
        except Exception as e:
            print("Error retrieving quote: {}".format(e))
            return None

        result = cursor.fetchone()

        if result is None:
            return None

        quote = cls(*result)
        connection.close()

        return quote

    def calculate_cost(self):
        if self.coverage_type == "Basic":
            cost = BASIC_RATE
        elif self.coverage_type == "Premium":
            cost = PREMIUM_RATE
        else:
            raise ValueError("Invalid coverage type: {}".format(self.coverage_type))
        
        if self.has_pet:
            cost += PET_PREMIUM
         
        if self.state == "California":
            tax_rate = CA_TAX
            if self.flood_coverage:
                cost += cost * CA_FLOOD
        elif self.state == "Texas":
            tax_rate = TX_TAX
            if self.flood_coverage:
                cost += cost * TX_FLOOD
        elif self.state == "New York":
            tax_rate = NY_TAX
            if self.flood_coverage:
                cost += cost * NY_FLOOD
        else:
            raise ValueError("Invalid state: {}".format(self))
         
        return cost

    @classmethod
    def rater(cls,uuid):
        quote = cls.get_by_uuid(uuid)
        cost = quote.calculate_cost()
        return {
            "Monthly Total": cost,
        }


