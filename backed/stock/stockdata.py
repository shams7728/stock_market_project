# Install yfinance if not already installed
# pip install yfinance

import yfinance as yf
from datetime import datetime, timedelta
import os

def download_indian_stocks(stock_list, start_date, end_date, folder_name="stock_data"):
    """
    Download historical stock data for multiple stocks and save each to a separate CSV file in a specific folder.
    
    Parameters:
        stock_list (list): List of stock ticker symbols.
        start_date (str): Start date in the format 'YYYY-MM-DD'.
        end_date (str): End date in the format 'YYYY-MM-DD'.
        folder_name (str): Name of the folder where files will be saved.
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")
    
    for ticker in stock_list:
        try:
            print(f"Downloading data for {ticker}...")
            # Download stock data
            data = yf.download(ticker, start=start_date, end=end_date)
            
            # Check if data is returned
            if not data.empty:
                # Define the file path
                file_path = os.path.join(folder_name, f"{ticker}_data.csv")
                
                # Save data to CSV
                data.to_csv(file_path)
                print(f"Data for {ticker} saved to {file_path}")
            else:
                print(f"No data found for {ticker}. Please check the ticker symbol.")
        except Exception as e:
            print(f"An error occurred for {ticker}: {e}")

if __name__ == "__main__":
    # Define the list of 25 Indian stock symbols (NSE format: 'TICKER.NS')
    stock_list = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "SBIN.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "ITC.NS",
        "KOTAKBANK.NS", "WIPRO.NS", "ADANIENT.NS", "LT.NS", "AXISBANK.NS",
        "MARUTI.NS", "ULTRACEMCO.NS", "TITAN.NS", "SUNPHARMA.NS", "HCLTECH.NS",
        "POWERGRID.NS", "TECHM.NS", "ASIANPAINT.NS", "NTPC.NS", "M&M.NS"
    ]
    
    # Define start and end dates (at least 3 years of data)
    end_date = datetime.now().strftime('%Y-%m-%d')  # Today's date
    start_date = (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d')  # 3 years ago
    
    # Download data
    download_indian_stocks(stock_list, start_date, end_date)
