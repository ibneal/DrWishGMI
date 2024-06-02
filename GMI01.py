import requests
import pandas as pd
import concurrent.futures
from datetime import datetime, timedelta
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

POLYGON_API_KEY = config['settings']['POLYGON_API_KEY']
TODAY_DATE = datetime(2024, 5, 31).date()  # Replace with the desired date


qqq_symbols = [
    "MSFT", "AAPL", "NVDA", "AMZN", "AVGO", "META", "GOOGL", "GOOG", "COST", "TSLA",
    "NFLX", "AMD", "PEP", "ADBE", "QCOM", "LIN", "CSCO", "TMUS", "INTU", "AMAT", "TXN", "AMGN", "CMCSA",
    "MU", "ISRG", "HON", "INTC", "BKNG", "LRCX", "VRTX", "REGN", "ADI", "ADP", "KLAC", "PANW", "MDLZ",
    "PDD", "SBUX", "SNPS", "MELI", "GILD", "ASML", "CDNS", "CRWD", "CTAS", "PYPL", "CEG", "NXPI", "MAR",
    "CSX", "ABNB", "ORLY", "MRVL", "MNST", "PCAR", "ROP", "CPRT", "WDAY", "MCHP", "MRNA", "DXCM", "AEP",
    "KDP", "ADSK", "FTNT", "AZN", "ROST", "PAYX", "KHC", "IDXX", "DASH", "LULU", "CHTR", "ODFL", "FAST",
    "EXC", "TTD", "GEHC", "CSGP", "DDOG", "VRSK", "FANG", "CCEP", "EA", "CTSH", "BIIB", "BKR", "ON", "XEL",
    "GFS", "CDW", "TEAM", "ANSS", "ZS", "MDB", "DLTR", "TTWO", "WBD", "ILMN", "WBA", "SIRI"
]

#Normalized list of the top 10 QQQ holding allocation to 100%
qqq_top_ten_holding = [
    {"ticker": "MSFT", "company_name": "Microsoft Corporation", "allocation": "100%"},
    {"ticker": "AAPL", "company_name": "Apple Inc.", "allocation": "14.11%"},
    {"ticker": "NVDA", "company_name": "NVIDIA Corporation", "allocation": "10.99%"},
    {"ticker": "AMZN", "company_name": "Amazon.com, Inc.", "allocation": "9.73%"},
    {"ticker": "META", "company_name": "Meta Platforms Inc Class A", "allocation": "8.22%"},
    {"ticker": "AVGO", "company_name": "Broadcom Inc.", "allocation": "7.73%"},
    {"ticker": "GOOGL", "company_name": "Alphabet Inc. Class A", "allocation": "4.94%"},
    {"ticker": "GOOG", "company_name": "Alphabet Inc. Class C", "allocation": "4.80%"},
    {"ticker": "COST", "company_name": "Costco Wholesale Corporation", "allocation": "4.41%"},
    {"ticker": "TSLA", "company_name": "Tesla, Inc.", "allocation": "4.10%"},
    {"ticker": "NFLX", "company_name": "Netflix, Inc.", "allocation": "3.39%"}
]

#Normalized list of the top 50 SPY holding allocation to 100%
spy_top_fifty_holding = [
    {"ticker": "MSFT", "company_name": "Microsoft Corporation", "allocation": "7.46%", "shares": "87,928,023"},
    {"ticker": "AAPL", "company_name": "Apple Inc", "allocation": "6.54%", "shares": "171,767,312"},
    {"ticker": "NVDA", "company_name": "NVIDIA Corporation", "allocation": "5.55%", "shares": "29,228,826"},
    {"ticker": "AMZN", "company_name": "Amazon.com, Inc.", "allocation": "4.04%", "shares": "108,168,699"},
    {"ticker": "META", "company_name": "Meta Platforms, Inc.", "allocation": "2.52%", "shares": "26,034,228"},
    {"ticker": "GOOGL", "company_name": "Alphabet Inc.", "allocation": "2.41%", "shares": "69,734,774"},
    {"ticker": "GOOG", "company_name": "Alphabet Inc.", "allocation": "2.03%", "shares": "58,383,586"},
    {"ticker": "BRK.B", "company_name": "Berkshire Hathaway Inc.", "allocation": "1.78%", "shares": "21,523,910"},
    {"ticker": "AVGO", "company_name": "Broadcom Inc.", "allocation": "1.50%", "shares": "5,209,462"},
    {"ticker": "LLY", "company_name": "Eli Lilly and Company", "allocation": "1.49%", "shares": "9,433,293"},
    {"ticker": "JPM", "company_name": "JPMorgan Chase & Co.", "allocation": "1.38%", "shares": "34,199,704"},
    {"ticker": "XOM", "company_name": "Exxon Mobil Corporation", "allocation": "1.26%", "shares": "53,408,799"},
    {"ticker": "TSLA", "company_name": "Tesla, Inc.", "allocation": "1.13%", "shares": "32,801,798"},
    {"ticker": "UNH", "company_name": "UnitedHealth Group Incorporated", "allocation": "1.12%", "shares": "10,941,795"},
    {"ticker": "V", "company_name": "Visa Inc.", "allocation": "1.05%", "shares": "18,723,640"},
    {"ticker": "PG", "company_name": "The Procter & Gamble Company", "allocation": "0.93%", "shares": "27,844,431"},
    {"ticker": "MA", "company_name": "Mastercard Incorporated", "allocation": "0.90%", "shares": "9,767,262"},
    {"ticker": "JNJ", "company_name": "Johnson & Johnson", "allocation": "0.86%", "shares": "28,480,604"},
    {"ticker": "COST", "company_name": "Costco Wholesale Corporation", "allocation": "0.82%", "shares": "5,252,919"},
    {"ticker": "HD", "company_name": "The Home Depot, Inc.", "allocation": "0.82%", "shares": "11,782,574"},
    {"ticker": "MRK", "company_name": "Merck & Co., Inc.", "allocation": "0.79%", "shares": "29,979,597"},
    {"ticker": "ABBV", "company_name": "AbbVie Inc.", "allocation": "0.69%", "shares": "20,886,943"},
    {"ticker": "CVX", "company_name": "Chevron Corporation", "allocation": "0.67%", "shares": "20,533,378"},
    {"ticker": "CRM", "company_name": "Salesforce, Inc.", "allocation": "0.66%", "shares": "11,459,656"},
    {"ticker": "BAC", "company_name": "Bank of America Corporation", "allocation": "0.64%", "shares": "81,455,806"},
    {"ticker": "NFLX", "company_name": "Netflix, Inc.", "allocation": "0.64%", "shares": "5,123,268"},
    {"ticker": "AMD", "company_name": "Advanced Micro Devices, Inc.", "allocation": "0.62%", "shares": "19,115,099"},
    {"ticker": "WMT", "company_name": "Walmart Inc.", "allocation": "0.61%", "shares": "50,631,810"},
    {"ticker": "PEP", "company_name": "PepsiCo, Inc.", "allocation": "0.59%", "shares": "16,266,416"},
    {"ticker": "KO", "company_name": "The Coca-Cola Company", "allocation": "0.59%", "shares": "46,035,604"},
    {"ticker": "TMO", "company_name": "Thermo Fisher Scientific Inc.", "allocation": "0.56%", "shares": "4,570,425"},
    {"ticker": "WFC", "company_name": "Wells Fargo & Company", "allocation": "0.54%", "shares": "42,605,038"},
    {"ticker": "ADBE", "company_name": "Adobe Inc.", "allocation": "0.53%", "shares": "5,350,865"},
    {"ticker": "QCOM", "company_name": "QUALCOMM Incorporated", "allocation": "0.53%", "shares": "13,168,631"},
    {"ticker": "LIN", "company_name": "Linde plc", "allocation": "0.50%", "shares": "5,736,833"},
    {"ticker": "CSCO", "company_name": "Cisco Systems, Inc.", "allocation": "0.48%", "shares": "48,104,869"},
    {"ticker": "MCD", "company_name": "McDonald's Corporation", "allocation": "0.48%", "shares": "8,581,542"},
    {"ticker": "ORCL", "company_name": "Oracle Corporation", "allocation": "0.47%", "shares": "18,875,018"},
    {"ticker": "ACN", "company_name": "Accenture plc", "allocation": "0.46%", "shares": "7,425,093"},
    {"ticker": "DIS", "company_name": "The Walt Disney Company", "allocation": "0.45%", "shares": "21,651,331"},
    {"ticker": "CAT", "company_name": "Caterpillar Inc.", "allocation": "0.44%", "shares": "6,034,976"},
    {"ticker": "INTU", "company_name": "Intuit Inc.", "allocation": "0.44%", "shares": "3,316,326"},
    {"ticker": "ABT", "company_name": "Abbott Laboratories", "allocation": "0.44%", "shares": "20,533,305"},
    {"ticker": "AMAT", "company_name": "Applied Materials, Inc.", "allocation": "0.44%", "shares": "9,850,474"},
    {"ticker": "GE", "company_name": "GE Aerospace", "allocation": "0.42%", "shares": "12,876,736"},
    {"ticker": "TXN", "company_name": "Texas Instruments Incorporated", "allocation": "0.42%", "shares": "10,745,178"},
    {"ticker": "DHR", "company_name": "Danaher Corporation", "allocation": "0.41%", "shares": "7,781,932"},
    {"ticker": "AMGN", "company_name": "Amgen Inc.", "allocation": "0.40%", "shares": "6,332,237"},
    {"ticker": "VZ", "company_name": "Verizon Communications Inc.", "allocation": "0.40%", "shares": "49,738,573"},
    {"ticker": "PFE", "company_name": "Pfizer Inc.", "allocation": "0.38%", "shares": "66,801,711"}
]

# Function to read symbols from a file and exclude any symbols containing a dot (.)
def read_symbols_from_file(file_path):
    with open(file_path, 'r') as file:
        symbols = [line.strip() for line in file.readlines() if '.' not in line]
    return symbols

# Read symbols from file
symbols_file_path = 'NYSEandNASDAQstocks.txt'
nyseNASDAQ_symbols = read_symbols_from_file(symbols_file_path)

def check_10_day_new_high_index(symbol):
        """
        Checks if the last closing price in the list of the previous 10 days is higher than the closing prices of the previous 9 days for each symbol and 
        calculates the total percentage of such stocks.

        Args:
        qqq_symbols (list): List of symbols of stocks in the QQQ index.

        Returns:
        float: Percentage of stocks that have made a new 10-day high.
        """
        # Function to fetch closing prices of the previous 10 days
        def get_previous_10_day_prices(symbol):
            end_date = TODAY_DATE - timedelta(days=1) if TODAY_DATE.weekday() == 0 else TODAY_DATE
            end_date -= timedelta(days=2 if end_date.weekday() == 6 else 1 if end_date.weekday() == 0 else 0)
            # Ensure end_date is not a weekend (if it happens to fall on a weekend after the adjustment)
            while end_date.weekday() > 4:  # 5 = Saturday, 6 = Sunday
                end_date -= timedelta(days=1)
            start_date = end_date - timedelta(days=15)  # Use 15 days to account for weekends
            endpoint = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}"
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    # Filter only the last 10 trading days
                    close_prices = [float(result["c"]) for result in data["results"]][-10:]
                    if len(close_prices) == 10:
                        return close_prices
            print(f"Error: Failed to fetch 10-day data for {symbol}. Status code: {response.status_code}")
            return None

        new_high_count = 0
        total_stocks = len(qqq_symbols)

        # Check if the last closing price is the highest for each symbol
        for symbol in qqq_symbols:
            close_prices = get_previous_10_day_prices(symbol)
            if close_prices and close_prices[-1] > max(close_prices[:-1]):
                new_high_count += 1

        if total_stocks > 0:
            return (new_high_count / total_stocks)
        else:
            return 0.0

# Function to fetch 52-week high data by fetching the last 52 weeks of daily close prices
def fetch_52_week_high(symbol):
    start_date = TODAY_DATE - timedelta(days=365)
    endpoint = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{today_date}?adjusted=true&apiKey={POLYGON_API_KEY}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            close_prices = [result['c'] for result in data['results']]
            high_52_week = max(close_prices)
            if close_prices[-1] >= high_52_week:
                return True
    return False

# Function to count new 52-week highs and write the tickers to a file
def count_new_52_week_highs(symbols):
    new_high_count = 0
    new_high_tickers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_symbol = {executor.submit(fetch_52_week_high, symbol): symbol for symbol in symbols}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                if future.result():
                    new_high_count += 1
                    new_high_tickers.append(symbol)
            except Exception as exc:
                print(f"Symbol {symbol} generated an exception: {exc}")

    # Write the tickers to a file
    filename = f"newHigh{TODAY_DATE.strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as file:
        for ticker in new_high_tickers:
            file.write(f"{ticker}\n")

    return new_high_count

def fetch_prices_and_compare(symbols, allocations, comparison_type='daily'):
    def get_last_trading_day():
        today = TODAY_DATE
        while today.weekday() > 4:  # Skip weekends
            today -= timedelta(days=1)
        return today

    def get_previous_trading_day():
        today = TODAY_DATE
        yesterday = today - timedelta(days=1)
        while yesterday.weekday() > 4:  # Skip weekends
            yesterday -= timedelta(days=1)
        return yesterday

    def get_last_week_close_date():
        today = TODAY_DATE
        if today.weekday() == 5:
            last_friday = today - timedelta(days=1)
        elif today.weekday() == 6:
            last_friday = today - timedelta(days=2)
        elif today.weekday() == 4:
            last_friday = today - timedelta(days=7)  # If today is Friday, return the previous Friday
        else:
            # For other weekdays, find the last Friday
            last_friday = today - timedelta(days=(today.weekday() - 4))
        return last_friday

    def fetch_close_price(symbol, date):
        date_str = date.strftime('%Y-%m-%d')
        endpoint = f"https://api.polygon.io/v1/open-close/{symbol}/{date_str}?adjusted=true&apiKey={POLYGON_API_KEY}"
        response = requests.get(endpoint)
        data = response.json()

        if 'close' in data:
            return data['close']
        else:
            print(f"Error: Failed to fetch closing price for {symbol} on {date_str}.")
            return None

    def calculate_weighted_sum(prices, allocations):
        weighted_sum = sum(price * allocation for price, allocation in zip(prices, allocations))
        return weighted_sum

    # Determine the dates for comparison
    if comparison_type == 'weekly':
        compare_date = get_last_week_close_date()
        reference_date = get_last_trading_day()
    else:
        compare_date = get_previous_trading_day()
        reference_date = get_last_trading_day()

    # Fetch the closing prices for the specified dates
    prices_compare_date = []
    prices_reference_date = []

    for symbol in symbols:
        close_price_compare = fetch_close_price(symbol, compare_date)
        close_price_reference = fetch_close_price(symbol, reference_date)
        if close_price_compare is not None and close_price_reference is not None:
            prices_compare_date.append(close_price_compare)
            prices_reference_date.append(close_price_reference)

    # Calculate the weighted sum of the closing prices for each day
    weighted_sum_compare_date = calculate_weighted_sum(prices_compare_date, allocations)
    weighted_sum_reference_date = calculate_weighted_sum(prices_reference_date, allocations)

    print(f"Weighted sum on {compare_date}: {weighted_sum_compare_date}")
    print(f"Weighted sum on {reference_date}: {weighted_sum_reference_date}")

    # Determine if the index closed positive or negative
    if weighted_sum_reference_date > weighted_sum_compare_date:
        print("The index closed positive.")
        return True
    else:
        print("The index closed negative.")
        return False


def main():
    positive_tally = 0
    negative_tally = 0

    print("QQQ 10 Day New High Index (Greater than or equal to 50%)")
    tenDayNewHighIndexResult = check_10_day_new_high_index(qqq_symbols)
    if tenDayNewHighIndexResult >= .5:
        print("YES")
        print(tenDayNewHighIndexResult)
        positive_tally+= 1
    else:
        print("NO")
        print(tenDayNewHighIndexResult)

    print("100 new 52-week highs were made in 6000+ stocks from NYSE")
    new_high_count = count_new_52_week_highs(nyseNASDAQ_symbols)
    if new_high_count >= 100:
        print(f"At least 100 new 52-week highs were made in US stocks. New high count: {new_high_count}")
        positive_tally+= 1
    else:
        print(f"Fewer than 100 new 52-week highs were made in US stocks. New high count: {new_high_count}")

    print("QQQ Daily TOP 10 HOLDINGS Index (DAILY CLOSE:)")
    symbols = [stock['ticker'] for stock in qqq_top_ten_holding]
    allocations = [float(stock['allocation'].strip('%')) / 100 for stock in qqq_top_ten_holding]
    positive_tally += 1 if fetch_prices_and_compare(symbols, allocations, comparison_type='daily') else 0


    print("SPY Daily TOP 50 HOLDINGS Index (DAILY CLOSE:)")
    symbols = [stock['ticker'] for stock in spy_top_fifty_holding]
    allocations = [float(stock['allocation'].strip('%')) / 100 for stock in spy_top_fifty_holding]
    positive_tally += 1 if fetch_prices_and_compare(symbols, allocations, comparison_type='daily') else 0


    print("QQQ Weekly TOP 10 HOLDINGS Index (WEEKLY CLOSE:)")
    symbols = [stock['ticker'] for stock in qqq_top_ten_holding]
    allocations = [float(stock['allocation'].strip('%')) / 100 for stock in qqq_top_ten_holding]
    positive_tally += 1 if fetch_prices_and_compare(symbols, allocations, comparison_type='weekly') else 0

    print("Manually check 0MUTI IBD Mutual Fund Above 50MA")
    print("Visit: https://research.investors.com/ibdchartsenlarged.aspx?cht=pvc&type=daily&symbol=0muti")

    print(str(positive_tally) + "/5")

    

if __name__ == "__main__":
    main()