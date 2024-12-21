import os
import pandas as pd
import yfinance as yf
from pymongo import MongoClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_financial_data(ticker):
    """
    Fetch financial data for a given ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "pe_ratio": info.get("trailingPE", "N/A"),
            "debt_to_equity_ratio": info.get("debtToEquity", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
            "price_to_book_ratio": info.get("priceToBook", "N/A"),
            "current_ratio": info.get("currentRatio", "N/A"),
            "operating_margin": info.get("operatingMargins", "N/A"),
            "net_profit_margin": info.get("profitMargins", "N/A"),
            "free_cash_flow": info.get("freeCashflow", "N/A"),
        }
    except Exception as e:
        logger.error(f"Error fetching financial data for {ticker}: {e}")
        return {}


def store_to_mongodb(folder_name="stock_data", db_name="stock_data", collection_name="stocks"):
    """
    Read CSV files containing stock data, fetch additional financial parameters,
    and store them in MongoDB.
    """
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://shamsmohd:mlJ17DRDPZmuY9Kj@stocks.xscx2.mongodb.net/?retryWrites=true&w=majority&appName=stocks")
    client = MongoClient(MONGO_URI)
    db = client[db_name]
    collection = db[collection_name]

    if not os.path.exists(folder_name):
        logger.error(f"Folder {folder_name} does not exist. Please create it and add the CSV files.")
        return

    for file_name in os.listdir(folder_name):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_name, file_name)
            logger.info(f"Processing file: {file_path}")

            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
                continue

            df["Close"] = pd.to_numeric(df.get("Close"), errors='coerce')
            df["Volume"] = pd.to_numeric(df.get("Volume"), errors='coerce')
            df.dropna(subset=["Close", "Volume"], inplace=True)

            if df.empty:
                logger.warning(f"File {file_name} is empty or contains invalid data.")
                continue

            ticker = file_name.split("_")[0]
            if not ticker.endswith(".NS"):
                ticker += ".NS"

            if df["Close"].iloc[-1] <= 0 or df["Volume"].iloc[-1] <= 0:
                logger.warning(f"Invalid data in file {file_name}. Skipping...")
                continue

            market_cap = df["Close"].iloc[-1] * df["Volume"].iloc[-1]
            financial_data = fetch_financial_data(ticker)

            stock_data = {
                "ticker": ticker.replace(".NS", ""),
                "market_cap": market_cap,
                **financial_data,
                "historical_data": df.to_dict(orient="records"),
            }

            try:
                collection.replace_one({"ticker": ticker.replace(".NS", "")}, stock_data, upsert=True)
                logger.info(f"Inserted or updated data for {ticker}.")
            except Exception as e:
                logger.error(f"Error inserting data for {ticker}: {e}")


if __name__ == "__main__":
    store_to_mongodb()
