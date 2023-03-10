Dependencies: 

1. ensure you have a mysql instance installed
2. ```pip3 install -r requirements.txt```
3. Set the following env vars:
```
export MYSQL_USER = your_user
export MYSQL_HOST = your_host
export MYSQL_PASSWORD = your_password
```
--------------------------------------------------
Setup Database:

    make setup

or 

    python3 main.py setup '{}'

--------------------------------------------------
Create:

    python3 main.py create '{"name": "Jane Smith", "coverage_type": "basic", "state": "CA", "has_pet": false, "flood_coverage": true}'


Retreive:

    python3 main.py retrieve '{"uuid": "7e4e8003-3093-4ac6-9fff-ac25fbd0f040"}'


Create State:

    python3 main.py create_rate '{"state": "UT", "state_tax_percent": 0.07, "flood_percent": 0.001, "default_rate":20, "premium_rate":40, "pet_rate":20}'


Update Rate:

    python3 main.py update_rate '{"state": "UT", "state_tax_percent": 0.085, "flood_percent": 0.001, "default_rate":20, "premium_rate":40, "pet_rate":20}'


Tests:

    python3 -m unittest test_quote.py
