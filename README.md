# lunar-calendar
English | [简体中文](./README.zh_CN.md)

Convert Chinese Lunar calendar date to and back from Gregorian calendar date between 1901-2100.

The Chinese Lunar calendar data is obtained from [Hong Kong Observatory][1]

## Usage
`lunar-calendar.sqlite` contains a table `gregorian_lunar` which contains the relationship of Gregorian calendar date to Chinese Lunar calendar date
for every single day between 1901-2100 scraped from  [Hong Kong Observatory][1] by `lunar_calendar.py`

- Lookup Gregorian date by Chinese Lunar date
```sql
SELECT gregorian_date FROM gregorian_lunar WHERE lunar_cycle = 1 AND lunar_year_of_cycle = 37 AND lunar_month_of_year = 10 AND lunar_day_of_month = 20;
```
- Lookup Chinese Lunar date by Gregorian date
```sql
SELECT lunar_cycle, lunar_year_of_cycle, lunar_month_of_year, lunar_day_of_month FROM gregorian_lunar WHERE gregorian_date = '2020-07-13';
SELECT lunar_cycle, lunar_year_of_cycle, lunar_year_of_cycle_name, lunar_month_of_year, lunar_month_of_year_name, lunar_day_of_month, lunar_day_of_month_name FROM gregorian_lunar_view WHERE gregorian_date = '2020-07-13';
```

`lunar-calendar.sqbpro` is a SQLite project file which contains demo usages.

## Credits
- [Hong Kong Observatory][1]
- [infinet/lunar-calendar](https://github.com/infinet/lunar-calendar)

## License
See [LICENSE](./LICENSE)

[1]: https://www.hko.gov.hk/tc/gts/time/conversion1_text.htm#