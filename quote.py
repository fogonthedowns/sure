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

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
          'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


class Rate:
    def __init__(self, state, state_tax_percent, flood_percent, default_cost, premium_cost, pet_cost):
        self.validate(state, state_tax_percent, flood_percent,
                      default_cost, premium_cost, pet_cost)
        self.state = state
        self.state_tax_percent = state_tax_percent
        self.flood_percent = flood_percent
        self.default_cost = default_cost
        self.premium_cost = premium_cost
        self.pet_cost = pet_cost

    def validate(self, state, state_tax_percent, flood_percent, default_cost, premium_cost, pet_cost):
        if not isinstance(state, str) or len(state) != 2:
            raise ValueError("'state' must be a string with 2 characters")
        if state not in STATES:
            raise ValueError("'state' must be a valid 2 letter state")
        if not isinstance(state_tax_percent, float) or state_tax_percent < 0:
            raise ValueError(
                "'state_tax_percent' must be a float with up to 4 decimal places and greater than or equal to 0")
        if not isinstance(flood_percent, float) or flood_percent < 0:
            raise ValueError(
                "'flood_percent' must be a float with up to 4 decimal places and greater than or equal to 0")
        if default_cost is not None and (not isinstance(default_cost, float) or default_cost <= 0):
            raise ValueError(
                "'default_cost' must be a float with up to 4 decimal places and greater than 0")
        if premium_cost is not None and (not isinstance(premium_cost, float) or premium_cost <= 0):
            raise ValueError(
                "'premium_cost' must be a float with up to 4 decimal places and greater than 0")
        if pet_cost is not None and (not isinstance(pet_cost, float) or pet_cost <= 0):
            raise ValueError(
                "'pet_cost' must be a float with up to 4 decimal places and greater than 0")
   
    @classmethod
    def load_rates_by_state(cls, state):
        cnx = create_connection()
        cursor = cnx.cursor()
        try:
            cursor.execute(
                "SELECT state, state_tax_percent, flood_percent, default_rate, premium_rate, pet_rate FROM rates WHERE state=%s",
                (state,)
            )
            rows = cursor.fetchall()
            if not rows:
                raise ValueError(f"No rates found for state '{state}'")
            row = rows[0]
            return cls(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]))
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def load_all_rates(cls):
        cnx = create_connection()
        cursor = cnx.cursor()
        query = "SELECT * FROM rates"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            rates = []
            for row in rows:
                print("foo")
                print(row)
                rate = cls(row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]))
                rates.append(rate)
            return rates
        except Error as e:
            print(e)
        finally:
            cursor.close()
            cnx.close()

class Quote:
    def __init__(self, name, coverage_type, state, has_pet, flood_coverage, uuidstr=None):
        self.validate_input(name, coverage_type, state,
                            has_pet, flood_coverage, uuidstr)
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
                raise ValueError(
                    "'{}' is a required attribute for Quote".format(attr_name))

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
            raise ValueError(
                "'coverage_type' must be either 'basic' or 'premium'")

    def save(self):
        connection = create_connection()
        cursor = connection.cursor()

        # Convert has_pet and flood_coverage to integers
        has_pet_int = 1 if self.has_pet == True else 0
        flood_coverage_int = 1 if self.flood_coverage == True else 0

        sql = "INSERT INTO quotes (uuid, name, coverage_type, state, has_pet, flood_coverage) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (str(self.uuid), self.name, self.coverage_type,
                  self.state, has_pet_int, flood_coverage_int)
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
            raise ValueError(
                "'uuid' must be a valid UUID in the format 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'")

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

        quote = cls(result[2], result[3], result[4],
                    result[5], result[6], result[1])
        connection.close()

        return quote

    def calculate_cost(self):
        rate = Rate.load_rates_by_state(self.state)
        
        if rate == None:
            raise ValueError(
                "Invalid state. State not yet supported: {}".format(self))
        
        if self.coverage_type == "BASIC":
            cost = rate.default_cost
        elif self.coverage_type == "PREMIUM":
            cost = rate.premium_cost
        else:
            raise ValueError(
                "Invalid coverage type: {}".format(self.coverage_type))

        if self.has_pet:
            cost += rate.pet_cost
        
        if self.flood_coverage:
            cost += cost * rate.flood_percent
        
        tax_rate = rate.state_tax_percent
        tax = tax_rate * cost
        total = cost + cost

        return {"subtotal": cost, "tax": tax, "total": total}

    @classmethod
    def rater(cls, uuid):
        quote = cls.get_by_uuid(uuid)
        cost = quote.calculate_cost()
        return {
            "monthly_total": cost,
        }
