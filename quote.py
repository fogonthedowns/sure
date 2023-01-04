import uuid
import re
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
    def __init__(self, name, coverage_type, state, has_pet, flood_coverage, uuidstr=None): 
        self.validate_input(name, coverage_type, state, has_pet, flood_coverage, uuidstr)
        if uuidstr == None:
            self.uuid = uuid.uuid4()
        else:
            self.uuid = uuidstr

        self.name = name
        self.coverage_type = coverage_type.upper()
        self.state = state
        self.has_pet = has_pet
        self.flood_coverage = flood_coverage
    
    def validate_input(self, name, coverage_type, state, has_pet, flood_coverage, uuidstr):
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
        
        # no need to validate further than this if class __init__ is invoked by Retrieve
        if uuidstr is not None:
            return
        if not isinstance(name, str):
            raise ValueError("'name' must be a string")
        if not isinstance(coverage_type, str):
            raise ValueError("'coverage_type' must be a string")
        if not isinstance(state, str) or len(state) != 2:
            raise ValueError("'state' must be a two-character string")
        if not isinstance(has_pet, bool):
            raise ValueError("'has_pet' must be a boolean")
        if not isinstance(flood_coverage, bool):
            raise ValueError("'flood_coverage' must be a boolean")
        if coverage_type.lower() not in ["basic", "premium"]:
            raise ValueError("'coverage_type' must be either 'basic' or 'premium'")

    def save(self):
        connection = create_connection()
        cursor = connection.cursor()
        
        # Convert has_pet and flood_coverage to integers
        has_pet_int = 1 if self.has_pet == True else 0
        flood_coverage_int = 1 if self.flood_coverage == True else 0
        
        sql = "INSERT INTO quotes (uuid, name, coverage_type, state, has_pet, flood_coverage) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (str(self.uuid), self.name, self.coverage_type, self.state, has_pet_int, flood_coverage_int)
        try:
            cursor.execute(sql, values)
        except Exception as e:
            print("Error saving quote: {}".format(e))
            return

        connection.commit()
        connection.close()

        return str(self.uuid)
    
    @classmethod
    def get_by_uuid(cls, uuid):
        # uuid validations
        if uuid is not None and not isinstance(uuid, str):
            raise ValueError("'uuid' must be a valid UUID")
        pattern = '^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
        if uuid is not None and not re.match(pattern, uuid):
            raise ValueError("'uuid' must be a valid UUID in the format 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'")
        
        # connect to the db
        connection = create_connection()
        cursor = connection.cursor()
        
        # query
        sql = "SELECT * FROM quotes WHERE uuid=%s"
        try:
            cursor.execute(sql, (uuid,))
        except Exception as e:
            print("Error retrieving quote: {}".format(e))
            return None

        result = cursor.fetchone()
        if result is None:
            return None

        quote = cls(result[2], result[3], result[4], result[5], result[6], result[1])
        connection.close()

        return quote

    def calculate_cost(self):
        if self.coverage_type == "BASIC":
            cost = BASIC_RATE
        elif self.coverage_type == "PREMIUM":
            cost = PREMIUM_RATE
        else:
            raise ValueError("Invalid coverage type: {}".format(self.coverage_type))
        
        if self.has_pet:
            cost += PET_PREMIUM
         
        if self.state == "CA":
            tax_rate = CA_TAX
            if self.flood_coverage:
                cost += cost * CA_FLOOD
        elif self.state == "TX":
            tax_rate = TX_TAX
            if self.flood_coverage:
                cost += cost * TX_FLOOD
        elif self.state == "NY":
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


