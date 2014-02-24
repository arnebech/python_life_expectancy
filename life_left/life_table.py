import csv
import os

class LifeTable(object):
    """simple load and row interpolation for life expectancy data"""

    def __init__(self):

        data = []

        csv_path = os.path.join(os.path.dirname(__file__), 'data.csv')

        with open(csv_path, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                for key in row:
                    row[key] = float(row[key])
                data.append(row)

            self.data = data

    def get_interpolated_row(self, age):
        """Returns interpolated data from our table"""

        if age < 0:
            raise Exception("Age cannot be negative")

        first_match = self.data[0]
        second_match = self.data[1]
        index = 2

        while (age > second_match['age']) and (index < len(self.data)):
            first_match = second_match
            second_match = self.data[index]
            index = index + 1

        if age > second_match['age']:
            #past our data, assume last point
            final_row = second_match.copy()
        else:
            fraction = (age - first_match['age']) / (second_match['age'] - first_match['age'])

            def interpolate(key):
                return (1 - fraction) * first_match[key] + fraction * second_match[key]

            final_row = {}
            for key in first_match:
                final_row[key] = interpolate(key)

        return final_row
