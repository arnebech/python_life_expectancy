"""Main api for interacting with life_left"""
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
import calendar

import life_left.life_table as life_table

table = life_table.LifeTable()

def get_fractional_age(birthday):
    """Returns fractional age (eg. 27.2) given a birthday (datetime)"""

    now = datetime.datetime.now()

    birth_stamp = calendar.timegm(birthday.utctimetuple())
    now_stamp = calendar.timegm(now.utctimetuple())

    time_delta = now_stamp - birth_stamp

    years = time_delta / (86400 * 365.25) #using avg year for simplicity

    return years


def get_info(birthday, gender='unknown'):
    """Retuns life expectancy info given a birthday in string or datetime
    format"""

    gender_values = ['male', 'female', 'unknown']

    if not gender in gender_values:
        return {
            'msg': 'Unknown gender "%s", expected: %s'
                % (gender, ', '.join(gender_values)),
            'success': False
        }

    if isinstance(birthday, basestring):
        birthday = parse(birthday)

    now = datetime.datetime.now()

    if birthday > now:
        return {
            'msg': 'Birthday cannot be in the future',
            'success': False
        }

    age = get_fractional_age(birthday)

    data = table.get_interpolated_row(age)

    years_left = data[gender]
    days_left = years_left * 365.25 #using avg year for simplicity
    hours_left = days_left * 24
    minutes_left = hours_left * 60
    seconds_left = minutes_left * 60

    total_life = age + years_left
    fraction_complete = age / total_life

    date_delta = relativedelta(now + relativedelta(seconds=seconds_left), now)

    return {
        'expected_age': total_life,
        'years_left': years_left,
        'days_left': days_left,
        'hours_left': hours_left,
        'minutes_left': minutes_left,
        'seconds_left': int(seconds_left),
        'date_left': {
            'years': date_delta.years,
            'months': date_delta.months,
            'days': date_delta.days,
            'hours': date_delta.hours,
            'minutes': date_delta.minutes,
            'seconds': date_delta.seconds
        },
        'age': age,
        'life_completed': fraction_complete,
        'success': True
    }
