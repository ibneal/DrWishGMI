import requests

POLYGON_API_KEY = 'NJyAkqptefQNLiUhNrnKqdR1g4yH_Kz6'

def fetch_nyse_tickers():
    tickers = []
    exchange = "XNAS"
    base_url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&exchange={exchange}&active=true&limit=1000&apiKey={POLYGON_API_KEY}"
    next_url = base_url
    
    while next_url:
        print(f"Fetching data from: {next_url}")
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            tickers.extend(ticker['ticker'] for ticker in data['results'] if 'type' in ticker and ticker['type'] in ['CS', 'ETF']) #Add FUND if doing XNYS
            next_cursor = data.get('next_url')
            if next_cursor:
                next_url = f"{next_cursor}&apiKey={POLYGON_API_KEY}"
            else:
                next_url = None
            print(f"Fetched {len(tickers)} tickers so far. Next URL: {next_url}")
        else:
            print(f"Error: Failed to fetch tickers. Status code: {response.status_code}")
            break

    return tickers

def save_tickers_to_file(tickers, file_path):
    with open(file_path, 'w') as file:
        for ticker in tickers:
            file.write(f"{ticker}\n")

# Fetch NASDAQ tickers and save to file
nyse_tickers = fetch_nyse_tickers()
output_file_path = 'XNAStockList.txt'
save_tickers_to_file(nyse_tickers, output_file_path)

print(f"Successfully saved {len(nyse_tickers)} tickers to {output_file_path}")
