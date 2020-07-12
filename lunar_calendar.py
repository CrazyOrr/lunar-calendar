import re
import sqlite3
import time
import urllib
import urllib.request

HKO_LUNAR_CALENDAR_YEARLY_URL_TEMPLATE = 'https://www.hko.gov.hk/tc/gts/time/calendar/text/files/T%dc.txt'
RE_CALENDER_LINE = re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日')

"""60 years for a cycle"""
cur_cycle = 0
"""year of cycle (0-59)"""
cur_year_of_cycle = 36
"""month of year (0-12), normally 12 months, every 2-3 years add 1 additional month"""
cur_month_of_year = 11
cur_month_of_year_name = '十一月'
"""day of month (0-29), 29 or 30 days a month"""
cur_day_of_month = 9
"""24 solar term (0-23)"""
cur_solar_term = 21

"""干支纪元"""
YEAR_OF_CYCLE = [
    '甲子',
    '乙丑',
    '丙寅',
    '丁卯',
    '戊辰',
    '己巳',
    '庚午',
    '辛未',
    '壬申',
    '癸酉',
    '甲戌',
    '乙亥',
    '丙子',
    '丁丑',
    '戊寅',
    '己卯',
    '庚辰',
    '辛巳',
    '壬午',
    '癸未',
    '甲申',
    '乙酉',
    '丙戌',
    '丁亥',
    '戊子',
    '己丑',
    '庚寅',
    '辛卯',
    '壬辰',
    '癸巳',
    '甲午',
    '乙未',
    '丙申',
    '丁酉',
    '戊戌',
    '己亥',
    '庚子',
    '辛丑',
    '壬寅',
    '癸卯',
    '甲辰',
    '乙巳',
    '丙午',
    '丁未',
    '戊申',
    '己酉',
    '庚戌',
    '辛亥',
    '壬子',
    '癸丑',
    '甲寅',
    '乙卯',
    '丙辰',
    '丁巳',
    '戊午',
    '己未',
    '庚申',
    '辛酉',
    '壬戌',
    '癸亥',
]
"""日期名称"""
DAY_OF_MONTH = [
    '初一',
    '初二',
    '初三',
    '初四',
    '初五',
    '初六',
    '初七',
    '初八',
    '初九',
    '初十',
    '十一',
    '十二',
    '十三',
    '十四',
    '十五',
    '十六',
    '十七',
    '十八',
    '十九',
    '二十',
    '廿一',
    '廿二',
    '廿三',
    '廿四',
    '廿五',
    '廿六',
    '廿七',
    '廿八',
    '廿九',
    '三十',
]
"""二十四节气"""
SOLAR_TERM = [
    '立春',
    '雨水',
    '惊蛰',
    '春分',
    '清明',
    '谷雨',
    '立夏',
    '小满',
    '芒种',
    '夏至',
    '小暑',
    '大暑',
    '立秋',
    '处暑',
    '白露',
    '秋分',
    '寒露',
    '霜降',
    '立冬',
    '小雪',
    '大雪',
    '冬至',
    '小寒',
    '大寒',
]


def main():
    conn = sqlite3.connect('lunar-calendar.sqlite')
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE gregorian_lunar (
        gregorian_date TEXT NOT NULL PRIMARY KEY,
        lunar_cycle INTEGER NOT NULL,
        lunar_year_of_cycle INTEGER NOT NULL,
        lunar_month_of_year INTEGER NOT NULL,
        lunar_month_of_year_name TEXT NOT NULL,
        lunar_day_of_month INTEGER NOT NULL,
        lunar_solar_term INTEGER
        )''')

    # for year in range(1901, 1902):
    for year in inclusive_range(1901, 2100):
        parse_hko(HKO_LUNAR_CALENDAR_YEARLY_URL_TEMPLATE % year, cursor)
        time.sleep(1)

    cursor.execute('''CREATE TABLE lunar_year_of_cycle (name TEXT NOT NULL)''')
    for year in YEAR_OF_CYCLE:
        cursor.execute('INSERT INTO lunar_year_of_cycle VALUES (?)', (year,))
    cursor.execute('''CREATE TABLE lunar_day_of_month (name TEXT NOT NULL)''')
    for day in DAY_OF_MONTH:
        cursor.execute('INSERT INTO lunar_day_of_month VALUES (?)', (day,))
    cursor.execute('''CREATE TABLE lunar_solar_term (name TEXT NOT NULL)''')
    for solar_term in SOLAR_TERM:
        cursor.execute('INSERT INTO lunar_solar_term VALUES (?)', (solar_term,))

    conn.commit()
    conn.close()


def inclusive_range(start: int, stop: int, step: int = 1):
    return range(start, stop + 1, step)


def parse_hko(page_url, cursor):
    """
    Parse lunar calendar from HK Obs
    :param page_url: Page URL for each one year between 1901-2100
    :param cursor: Database cursor
    """
    print('Reading and parsing %s' % page_url)
    with urllib.request.urlopen(page_url) as f:
        for line in f:
            decoded_line = line.decode('big5')
            m = RE_CALENDER_LINE.match(decoded_line)
            if m is None:
                continue
            fields = decoded_line.split()

            # gregorian_date_name = fields[0]
            year = m.group(1).zfill(4)
            month_of_year = m.group(2).zfill(2)
            day_of_month = m.group(3).zfill(2)
            gregorian_date = "%s-%s-%s" % (year, month_of_year, day_of_month)

            lunar_date = fields[1]
            global cur_day_of_month
            if lunar_date.endswith('月'):
                # new month
                global cur_month_of_year, cur_month_of_year_name

                if lunar_date == '正月':
                    # new year
                    global cur_year_of_cycle
                    cur_year_of_cycle = (cur_year_of_cycle + 1) % 60
                    if cur_year_of_cycle == 0:
                        # new cycle
                        global cur_cycle
                        cur_cycle += 1
                    cur_month_of_year = 0
                else:
                    cur_month_of_year += 1

                cur_month_of_year_name = lunar_date
                # lunar_date = '初一'
                cur_day_of_month = 0
            else:
                cur_day_of_month += 1

            solar_term = fields[3] if len(fields) > 3 else None
            if solar_term is not None:
                global cur_solar_term
                cur_solar_term = (cur_solar_term + 1) % 24

            # print("%s cycle:%d year:%d month:%d(%s) day:%d(%s) %s" % (
            #     gregorian_date, cur_cycle, cur_year_of_cycle, cur_month_of_year, cur_month_of_year_name,
            #     cur_day_of_month, lunar_date, solar_term))
            cursor.execute('INSERT INTO gregorian_lunar VALUES (?, ?, ?, ?, ?, ?, ?)', (
                gregorian_date, cur_cycle, cur_year_of_cycle, cur_month_of_year, cur_month_of_year_name,
                cur_day_of_month, None if solar_term is None else cur_solar_term
            ))


if __name__ == '__main__':
    main()
