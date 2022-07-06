import csv
from datetime import datetime
from sqlalchemy import null


# Used to create a timestamp when a query is made, for now prints to terminal
def get_timestamp():
    dt = datetime.now()
    dt_now = str(dt)
    return dt_now[:-7]


# Write to csv file
def log_partial_to_csv(term: str, postcode_list: list, date: str):
    with open('App/results.csv', 'a', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([term.upper(), len(postcode_list), date])
        print(f'{term}, {len(postcode_list)}, {date}')


# Write to csv file
def log_full_to_csv(postcode: str, date: str):
    with open('App/results.csv', 'a', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([postcode.upper(), 1, date])
        print(f'{postcode}, 1, {date}')


def format_address(address):
    tmp_dict = {}
    final_address = []

    for i in range(len(address)):
        # Taking first dict from the list and looping through that
        tmp_dict = address[i]
        # Looping through the vals in tmp_dict and adding them to a new list
        pulled_address = [tmp_dict[v] for v in tmp_dict if type(tmp_dict[v]) != type(null)]
        # Pull the building number to a tmp variable
        tmp_building_num = pulled_address[0]
        # Check to see if the first item (building number) starts with 0000, if it does delete it
        if tmp_building_num.startswith('0000'):
            pulled_address.pop(0)
        # Check to see it the first item (building number) starts with 000
        elif tmp_building_num.startswith('000'):
            pulled_address[0] = tmp_building_num[3:]
        # Check to see it the first item (building number) starts with 00
        elif tmp_building_num.startswith('00'):
            pulled_address[0] = tmp_building_num[2:]
        # Check to see it the first item (building number) starts with 0
        elif tmp_building_num.startswith('0'):
            pulled_address[0] = tmp_building_num[1:]
        # Concatenate string to make a single address string, if value is none ignore it
        res = ' '.join(filter(lambda x: x if x is not None else '', pulled_address))
        # Insert new string into final_list
        final_address.insert(i, res)
        # Clear the tmp_dict
        tmp_dict.clear()
        # Clear res
        res = ''

    return final_address

