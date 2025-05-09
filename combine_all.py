import pandas as pd
import pytz
from datetime import datetime
import requests
import asyncio
import os

dataset_id = "d_4e19214c3a5288eab7a27235f43da4fa"
url = "https://data.gov.sg/api/action/datastore_search?resource_id=" + dataset_id

response = requests.get(url)

def get_dayname(date_str):
    mapping = dict(map(lambda x: (x['date'], x['holiday']), response.json()['result']['records']))
    # Parse the date string to a naive datetime object
    naive_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    if str(naive_datetime.date()) in mapping:
        return mapping[str(naive_datetime.date())]
    # Localize the naive datetime object to Singapore Time
    # Get the day name
    day_name = naive_datetime.strftime("%A")
    return day_name

async def round_to_nearest_minute(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.round('min')
    return df

async def main():
    df1 = pd.read_csv(r'combined_data\telegram_messages.csv', encoding='latin1')
    df2 = pd.read_csv(r'combined_data\motor_traffic_data.csv', encoding='latin1')
    df3 = pd.read_csv(r'combined_data\train_data.csv', encoding='latin1')
    merged_df = pd.DataFrame(columns=['Date', "Message", "Classification", 'Name', 'Johor', 'Woodlands', 'Tuas', 'Availability'])

    df3['Date'] = pd.to_datetime(df3['Date'] + ' ' + df3['Time'])
    df2.rename(columns={'date': "Date"}, inplace=True)
    df1 = df1[['Date', 'Message', 'Classification']]

    df1 = await round_to_nearest_minute(df1)
    df2 = await round_to_nearest_minute(df2)
    df3 = await round_to_nearest_minute(df3)
    df1.drop_duplicates(inplace=True)

    for row in range(len(df1)):
        new_row = {
            "Date": df1.iloc[row]["Date"],
            "Message": df1.iloc[row]["Message"],
            "Classification": df1.iloc[row]["Classification"],
            "Name": None,
            "Johor": None,
            "Woodlands": None,
            "Tuas": None,
            "Availability": None
        }
        # Append the new row to merged_df
        merged_df = pd.concat([merged_df, pd.DataFrame([new_row])], ignore_index=True)

    for row in range(len(df2)):
        if df2.iloc[row]['Date'] in merged_df['Date'].values:
            merged_df.loc[merged_df['Date'] == df2.iloc[row]['Date'], 'Johor'] = df2.iloc[row]['johor']
            merged_df.loc[merged_df['Date'] == df2.iloc[row]['Date'], 'Woodlands'] = df2.iloc[row]['woodlands']
            merged_df.loc[merged_df['Date'] == df2.iloc[row]['Date'], 'Tuas'] = df2.iloc[row]['tuas']
        else:
            new_row = {
                "Date": df2.iloc[row]['Date'],
                "Message": None,
                "Classification": None,
                "Johor": df2.iloc[row]['johor'],
                "Woodlands": df2.iloc[row]['woodlands'],
                "Tuas": df2.iloc[row]['tuas'],
                "Availability": None
            }
            merged_df = pd.concat([merged_df, pd.DataFrame([new_row])], ignore_index=True)

    for row in range(len(df3)):
        if df3.iloc[row]['Date'] in merged_df['Date'].values:
            merged_df.loc[merged_df['Date'] == df3.iloc[row]['Date'], 'Availability'] = df3.iloc[row]['Availability']
        else:
            new_row = {
                "Date": df3.iloc[row]['Date'],
                "Message": None,
                "Classification": None,
                "Name": None,
                "Johor": None,
                "Woodlands": None,
                "Tuas": None,
                "Availability": df3.iloc[row]['Availability']
            }
            merged_df = pd.concat([merged_df, pd.DataFrame([new_row])], ignore_index=True)

    merged_df = merged_df.sort_values(by='Date').reset_index(drop=True)
    merged_df['Day'] = merged_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S').apply(get_dayname)

    dir_path = r'combined_data'
    merged_df.to_csv(os.path.join(dir_path, 'merged_data.csv'), index=False)

if __name__ == '__main__':
    asyncio.run(main())