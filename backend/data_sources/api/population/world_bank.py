import requests

def fetch_population_data(countryCode, start_year, end_year):
    url = (
        f"https://api.worldbank.org/v2/country/{countryCode}/indicator/SP.POP.TOTL"
        f"?format=json&date={start_year}:{end_year}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"World Bank API error: {response.status_code} - {response.text}")


    
 

# Test
if __name__ == "__main__":
    country_code = "CN"  
    start_year = 1960
    end_year = 2022

    raw_data = fetch_population_data(country_code, start_year, end_year)
    print("Raw Population Data:")
    print(raw_data)
    