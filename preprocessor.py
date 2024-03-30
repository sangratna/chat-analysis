import pandas as pd
import re

def preprocess(data):
    pattern = r'(\d+/\d+/\d+), (\d+:\d+\s*[AP]M) - (.*)'
    messages = re.findall(pattern, data)

    df = pd.DataFrame(messages, columns=['Date', 'Time', 'Message'])
    df['DateTime'] = pd.to_datetime(df['Date'] + ', ' + df['Time'], format='%m/%d/%y, %I:%M %p')

    users = []
    messages = []

    for message in df['Message']:
        entry = re.split('([\w\s]+?):\s', message)
        if len(entry) > 1:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df['DateTime'] = df['Date'] + ', ' + df['Time']
    # Convert the concatenated column to datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%y, %I:%M %p')
    df['year'] = df['DateTime'].dt.year
    df['month_num'] = df['DateTime'].dt.month
    df['month'] = df['DateTime'].dt.month_name()
    df['day'] = df['DateTime'].dt.day
    df['day_name'] = df['DateTime'].dt.day_name()
    df['day_name'] = df['DateTime'].dt.day_name()
    df['hour'] = df['DateTime'].dt.hour
    df['minute'] = df['DateTime'].dt.minute

    # Drop the original 'Message' column if needed
    df.drop('Message', axis=1, inplace=True)

    return df
