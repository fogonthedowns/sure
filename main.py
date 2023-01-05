import argparse
import json

import quote
from quote import Quote
from db import delete_all_rates, insert_initial_data, create_connection, create_table, create_rate_table


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description='Create or retrieve a quote from the Acme homeowners insurance database')
    # Add the action argument (either 'create' or 'retrieve')
    parser.add_argument('action', type=str, choices=[
                        'create', 'retrieve', 'setup'], help='Action to perform')
    # Add the JSON data argument
    parser.add_argument('data', type=json.loads,
                        help='JSON data for the quote')
    # Parse the arguments
    args = parser.parse_args()


    # Check the action
    if args.action == 'create':
        # Create the quote and save it to the database
        q = Quote(**args.data)
        uuid = q.save()
        print(f'Quote created with UUID: {uuid}')
    elif args.action == 'retrieve':
        # Retrieve the quote from the database
        q = Quote.get_by_uuid(**args.data)
        quote = Quote.rater(**args.data)
        print(f'Retrieved quote: {q.__dict__} \nwith cost: {quote}')
    elif args.action == 'setup':
        # Create the connection and table (if they don't already exist)
        conn = create_connection()
        create_table(conn)
        create_rate_table(conn)
        delete_all_rates(conn)
        insert_initial_data(conn)


if __name__ == '__main__':
    main()
