## Life Left

A simple project to get more familiar with python. 

Given a birthdate (string or datetime) it will return expected life expectancy and "time left" in different formats. Obiviously, they are estimates. Data was gathered from [NCHS](http://www.cdc.gov/nchs/data/nvsr/nvsr61/nvsr61_06.pdf)

Sample usage:

```python
import life_left
import pprint

info = life_left.get_info('20 April 1986', 'male')
pprint.pprint(info)
```

Sample output:
```python
{'age': 27.85061899510736,
 'date_left': {'days': 17,
               'hours': 17,
               'minutes': 33,
               'months': 10,
               'seconds': 21,
               'years': 49},
 'days_left': 18217.73149907407,
 'expected_age': 77.72804951960859,
 'hours_left': 437225.5559777777,
 'life_completed': 0.35830847637674784,
 'minutes_left': 26233533.358666662,
 'seconds_left': 1574012001,
 'success': True,
 'years_left': 49.87743052450122}
 ```

