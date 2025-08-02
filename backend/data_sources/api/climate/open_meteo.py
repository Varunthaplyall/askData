import requests
import pandas as pd 

def fetch_climate_data(location, start_date, end_date):
    lat = location['lat']
    lon = location['long']


    url = (
        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=auto"
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.json() 
        # data = response.json()
        # daily_data = data['daily']
        # df = pd.DataFrame(data=daily_data)        
        # df['time'] = pd.to_datetime(df['time'])
        # df.set_index('time', inplace=True)
        
        # return df
    else:
        raise Exception(f"Open-Meteo API error: {response.status_code} - {response.text}")







# Test
if __name__ == "__main__":
    delhi_location = {
        'country_code': 'IN',
        'name': 'Delhi',
        'lat': 28.6139,
        'long': 77.2090
    }

    # Get the data as a DataFrame
    climate_df = fetch_climate_data(delhi_location, "2023-01-01", "2023-01-10")
    # climate_df.to_csv("climate_data_delhi.csv")
    print("--- Climate Data for Delhi (First 5 Days) ---")
    print(climate_df)