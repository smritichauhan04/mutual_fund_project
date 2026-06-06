import os
import requests
import pandas as pd
import time

data_dir = "data/raw/"

target_schemes = {
    "125497": "HDFC Top 100 Direct",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip"
}

print("STARTING LIVE NAV DATA EXTRACTION VIA API")
print("-" * 60)

for amfi_code, fund_name in target_schemes.items():
    print(f"Fetching data for: {fund_name} (Code: {amfi_code})...")
    url = f"https://api.mfapi.in/mf/{amfi_code}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if "data" in json_data and len(json_data["data"]) > 0:
                df = pd.DataFrame(json_data["data"])
                df['amfi_code'] = amfi_code
                df = df[['amfi_code', 'date', 'nav']]
                
                file_name = f"live_nav_{amfi_code}.csv"
                file_path = os.path.join(data_dir, file_name)
                df.to_csv(file_path, index=False)
                print(f"Success: Saved records to {file_name}")
            else:
                print(f"Warning: No data found for {amfi_code}.")
        else:
            print(f"Failed to fetch {amfi_code}. Status: {response.status_code}")
    except Exception as e:
        print(f"Error processing {amfi_code}: {e}")
        
    time.sleep(1)

print("API Extraction Complete.")