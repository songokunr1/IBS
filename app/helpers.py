from datetime import date, timedelta
import datetime as dt



def get_date_info(date_string):
    datetime = dt.datetime.strptime(date_string, "%Y-%m-%d")
    date_info = {
        'previous': str(datetime + timedelta(days=-1))[:10],
        'next': str(datetime + timedelta(days=1))[:10],
        'today': datetime,
        'week_name': datetime.strftime("%A"),
        'info': str(datetime.strftime("%A")) + ' ' + str(datetime)[:10]
    }
    return date_info

