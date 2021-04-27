from datetime import datetime

# Custom Validators
def convert_date_formats(date):
    date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    return date