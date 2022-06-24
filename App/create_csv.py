import csv
from datetime import datetime


def test_csv():

    # Open the file in write mode
    with open('results.csv', 'w', encoding='UTF-8') as file:
        # Create a csv writer
        writer = csv.writer(file)

        # Write a row to the csv file
        writer.writerow(['Searched Postcode', 'Number of results', 'Date Time'])



test_csv()


