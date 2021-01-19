from connection import cursor
import datetime

#Weather table column names
column_names = ['timestamp', 'air_pressure', 'air_temperature', 'max_wind_speed', 'max_wind_direction',
'min_wind_speed', 'min_wind_direction']

def test_query():
    cursor.execute('SELECT TOP 10 * FROM [JSONServer].[dbo].[Weather]')
    rows = cursor.fetchall()
    return rows

def get_cursor_description():
    print(cursor.description)


#Convert row into a dictionary
def fecthone_dict(row, multiple):
    data_entry = {}
    if not multiple:
        data_entry['status'] = 'Ok'
    for col in range(0, len(column_names)):
        row_element = datetime_to_string(row[col])
        data_entry[column_names[col]] = row_element
    return data_entry


#Convert all rows from a fetch into a list of dictionaries
def fecthall_dict(rows):
    fetch_result = []

    for row in rows:
        fetch_result.append(fecthone_dict(row, True))
    return fetch_result


#Query for 'get_current' service. 
def get_current_query():
    query = 'SELECT TOP 1 * FROM [JSONServer].[dbo].[Weather] ORDER BY timestamp DESC'
    cursor.execute(query)
    row = cursor.fetchall()
    row_dict = fecthone_dict(row[0], False)
    print(row_dict)
    return row_dict

#Query for 'get_range' service.
def get_range_query(start_date, end_date):

    response = {}
    
    if (start_date > end_date): start_date, end_date = end_date, start_date
    query = f"SELECT * FROM [JSONServer].[dbo].[Weather] WHERE timestamp BETWEEN {start_date} AND {end_date}"
    print(query)

    cursor.execute(query)
    rows = cursor.fetchall()
    rows_dict = fecthall_dict(rows)
    print(rows_dict)

    response['status'] = 'OK'
    response['num_records'] = len(rows_dict)
    response['data'] = rows_dict
    return response

#Parse datetime object into a string
def datetime_to_string(object):
    if isinstance(object, datetime.datetime):
        return object.__str__()
    return object

def lowest_date():
    cursor.execute('SELECT TOP 1 timestamp FROM [JSONServer].[dbo].[Weather] ORDER BY timestamp ASC')
    lowest = cursor.fetchone()
    print(lowest[0])
    return lowest[0]
