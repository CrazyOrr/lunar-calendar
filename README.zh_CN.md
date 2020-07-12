# lunar-calendar
[English](./README.md) | 简体中文

查询转换1901-2100间的公历日期与中国农历日期

中国农历数据来自于[香港天文台][1]

## 使用
`lunar-calendar.sqlite`为SQLite数据库文件，其中包含`gregorian_lunar`表，表中的数据项为1901-2100年间每一天的公历日期与中国农历日期的对应关系，
这些数据是由`lunar_calendar.py`从[香港天文台][1]网站抓取的。

- 由中国农历日期查询对应的公历日期
```sql
SELECT gregorian_date FROM gregorian_lunar WHERE lunar_cycle = 1 AND lunar_year_of_cycle = 37 AND lunar_month_of_year = 10 AND lunar_day_of_month = 20;
```
- 由公历日期查询对应的中国农历日期
```sql
SELECT lunar_cycle, lunar_year_of_cycle, lunar_month_of_year, lunar_day_of_month, lunar_solar_term FROM gregorian_lunar WHERE gregorian_date = '2020-07-06';
SELECT lunar_cycle, lunar_year_of_cycle, lunar_year_of_cycle_name, lunar_month_of_year, lunar_month_of_year_name, lunar_day_of_month, lunar_day_of_month_name, lunar_solar_term, lunar_solar_term_name FROM gregorian_lunar_view WHERE gregorian_date = '2020-07-06';
```

`lunar-calendar.sqbpro`是SQLite工程文件，其中包含了以上的使用演示。

## 致谢
- [香港天文台][1]
- [infinet/lunar-calendar](https://github.com/infinet/lunar-calendar)

## 许可
见[LICENSE](./LICENSE)

[1]: https://www.hko.gov.hk/tc/gts/time/conversion1_text.htm#