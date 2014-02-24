import unittest
import datetime
from dateutil.relativedelta import relativedelta

from life_left import api, life_table

table = life_table.LifeTable()

sample_birthday_string = '20 April 1986'
sample_birthday = datetime.datetime(1986, 4, 20)

class LifeLeftTest(unittest.TestCase):

    def test_table_negative_age(self):
        with self.assertRaises(Exception):
            table.get_interpolated_row(-1)

    def test_table_old_age(self):
        #once we get past max age, we return the last life expectancy
        row = table.get_interpolated_row(200)
        row2 = table.get_interpolated_row(300)
        self.assertEqual(row, row2)

    def test_table_row(self):
        row = table.get_interpolated_row(50)
        self.assertEqual(row, {
            "age": 50,
            "unknown": 31.5,
            "male": 29.6,
            "female": 33.2
        })

    def test_table_interpolate_row(self):
        row = table.get_interpolated_row(12)
        self.assertEqual(row, {
            "age": 12,
            "unknown": 67.34,
            "male": 64.94,
            "female": 69.64
        })

    def test_fractional_age(self):
        now = datetime.datetime.now()
        years_ago = now - relativedelta(days=700)
        age = api.get_fractional_age(years_ago)
        expected_age = 700 / 365.25
        self.assertAlmostEqual(age, expected_age)

    def test_success(self):
        info = api.get_info(sample_birthday_string)
        self.assertEqual(info['success'], True)

    def test_gender_wrong(self):
        info = api.get_info(sample_birthday_string, 'cat')
        self.assertEqual(info['success'], False)

    def test_birthday_future(self):
        info = api.get_info('20 April 2500')
        self.assertEqual(info['success'], False)

    def test_gender_difference(self):
        info_unknown = api.get_info(sample_birthday_string)
        info_male = api.get_info(sample_birthday_string, 'male')
        info_female = api.get_info(sample_birthday_string, 'female')
        self.assertNotEqual(round(info_unknown['hours_left']), round(info_male['hours_left']))
        self.assertNotEqual(round(info_unknown['hours_left']), round(info_female['hours_left']))
        self.assertNotEqual(round(info_male['hours_left']), round(info_female['hours_left']))

    def test_datetime_argument(self):
        info = api.get_info(sample_birthday)
        info2 = api.get_info(sample_birthday_string)
        self.assertEqual(round(info['hours_left']), round(info2['hours_left']))
        self.assertEqual(round(info['age'], 4), round(info2['age'], 4))

    def test_contains_properties(self):
        info = api.get_info(sample_birthday_string)

        assert 'years_left' in info
        assert 'days_left' in info
        assert 'hours_left' in info
        assert 'minutes_left' in info
        assert 'seconds_left' in info
        assert 'date_left' in info
        assert 'age' in info
        assert 'life_completed' in info
        assert 'success' in info

        assert 'years' in info['date_left']
        assert 'months' in info['date_left']
        assert 'days' in info['date_left']
        assert 'hours' in info['date_left']
        assert 'minutes' in info['date_left']
        assert 'seconds' in info['date_left']

def run():
    unittest.main(module=__name__)
