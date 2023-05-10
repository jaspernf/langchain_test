import re
from datetime import datetime


def check_date_validity(date, impact=None , format_accuracy=None):
    """parse date from a string"""
    try:
        if len(date.split(' ')) > 6:
            d = re.findall(r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]', date)
            date = d[0]
    except:
        pass

    if 'day' in date.lower():
        temp_date = ''
        for d in date.split(' '):
            if 'day' in d.lower():
                continue
            temp_date += f' {d}'
        date = temp_date.strip()

    if 'august' in date.lower():
        date = date.strip().replace('th', '').replace('nd', '').replace('rd', '')
    else:
        date = date.strip().replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
    if len(date) == 8 or len(date) == 7:
        if '/' in date:
            if len(date.split('/')[2]) == 2:
                date = f"{date.split('/')[0]}/{date.split('/')[1]}/20{date.split('/')[2]}"
                if impact != None:
                    impact += 2
        if '.' in date:
            date = f"{date.split('.')[0]}/{date.split('.')[1]}/20{date.split('.')[2]}"
            if impact != None:
                impact += 2
    for d_ft in ['%b %d, %Y', '%d %b %Y', '%b. %d, %Y', '%b %d %Y',
                 '%B %d %Y', '%B %d, %Y', '%B %Y', '%B %m, %Y', '%d %B %Y',
                 '%B, %d, %Y',
                 '%d/%m/%Y', '%d.%m.%Y', '%m/%d/%Y',
                 '%Y-%m-%d', '%Y-%d-%m', '%d-%m-%Y']:
        try:
            if '%b' in d_ft:
                date = date.lower()
            if '%B' in d_ft:
                date = date.title()

            date = datetime.strptime(date, d_ft)
            if any(x == d_ft for x in ['%Y-%m-%d', '%Y-%d-%m', '%m/%d/%Y',
                                       '%d/%m/%Y', '%d.%m.%Y', '%m-%d-%Y']):
                if date.month < 13 and date.day < 13:
                    if date.month == date.day:
                        return True
                    else:
                        return False
                else:
                    return True
            return True
        except Exception as e:
            pass
    return False

def convert_date_string(date, impact=None , format_accuracy=None):
    """parse date from a string"""
    try:
        if len(date.split(' ')) > 6:
            d = re.findall(r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]', date)
            date = d[0]
    except:
        pass

    if 'day' in date.lower():
        temp_date = ''
        for d in date.split(' '):
            if 'day' in d.lower():
                continue
            temp_date += f' {d}'
        date = temp_date.strip()

    if 'august' in date.lower():
        date = date.strip().replace('th', '').replace('nd', '').replace('rd', '')
    else:
        date = date.strip().replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
    if len(date) == 8 or len(date) == 7:
        if '/' in date:
            if len(date.split('/')[2]) == 2:
                date = f"{date.split('/')[0]}/{date.split('/')[1]}/20{date.split('/')[2]}"
                if impact != None:
                    impact += 2
        if '.' in date:
            date = f"{date.split('.')[0]}/{date.split('.')[1]}/20{date.split('.')[2]}"
            if impact != None:
                impact += 2
    for d_ft in ['%b %d, %Y', '%d %b %Y', '%b. %d, %Y', '%b %d %Y',
                 '%B %d %Y', '%B %d, %Y', '%B %Y', '%B %m, %Y', '%d %B %Y',
                 '%B, %d, %Y',
                 '%d/%m/%Y', '%d.%m.%Y', '%m/%d/%Y',
                 '%Y-%m-%d', '%Y-%d-%m', '%d-%m-%Y', '%m-%d-%Y']:
        try:
            if '%b' in d_ft:
                date = date.lower()
            if '%B' in d_ft:
                date = date.title()

            date = datetime.strptime(date, d_ft)
            return date
        except Exception as e:
            pass
    raise ValueError('Date cannot be Parsed!')