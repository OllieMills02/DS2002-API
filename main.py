import requests
import json
import pandas as pd


def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list):
            country_data = data[0]  # Take the first result if there are multiple
            return country_data.get("capital"), country_data.get("population")
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None, None


def main():
    while True:
        country_name = input("Enter a country name (or type 'exit' to quit): ").strip()
        if country_name.lower() == "exit":
            break

        capital, population = get_country_info(country_name)
        if capital is not None and population is not None:
            print(f"Capital: {capital}")
            print(f"Population: {population}")

            # Store data in a dataframe
            df = pd.DataFrame({'Country': [country_name], 'Capital': [capital], 'Population': [population]})

            # Load existing data
            try:
                with open("country_data.json", "r") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []

            # Append new data
            existing_data.append(df.to_dict(orient='records')[0])

            # Write data to JSON file
            with open("country_data.json", "w") as f:
                json.dump(existing_data, f, indent=4)

        else:
            print("Country information not found. Please enter a valid country name.")


if __name__ == "__main__":
    main()