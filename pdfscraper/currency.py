currency = {
    '£': 'GBP',
    '$': 'USD',
    '€': 'EUR',
}

def get_currency_abbreviation(data):
    """Return currency value depends on the input data
    this function checks the sign of the data
    """
    for k, val in currency.items():
        if k in data:
            return val

def check_if_currency(data):
    """Checking if the inputed data is an amount in currency"""
    has_symbol_check = False
    is_number_check = False
    for c in currency.keys():
        if c in data:
            has_symbol_check = True
            data = data.replace(c, '')
    if data.replace('.', '').replace(',', '').isdigit() is True:
        is_number_check = True

    return True if has_symbol_check is True and is_number_check is True else False

def _parse_string(val):
    parsed_val = ''
    for c in val:
        if c == '.':
            parsed_val += '.'
        if c == ',':
            parsed_val += ','
    return parsed_val


def clean_currency(data):
    """:return currency value and remove all symbols and decimal places"""
    abv = get_currency_abbreviation(data)
    new_data = data
    for c in currency.keys():
        new_data = new_data.replace(c, '')
    if abv == 'EUR':
        try:
            if ',' in new_data:
                arr = new_data.split(',')
                if int(arr[1]) != 0:
                    new_data = f'{arr[0]}.{arr[1]}'
                else:
                    new_data = arr[0]
                new_data = new_data.replace('.', '')
        except:
            if '.' in new_data:
                arr = new_data.split('.')
                if int(arr[1]) != 0:
                    new_data = f'{arr[0]}.{arr[1]}'
                else:
                    new_data = arr[0]
                new_data = new_data.replace(',', '')
    else:
        if '.' in new_data:
            arr = new_data.split('.')
            if int(arr[1]) != 0:
                new_data = f'{arr[0]}.{arr[1]}'
            else:
                new_data = arr[0]
            new_data = new_data.replace(',', '')
    return new_data