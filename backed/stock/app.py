from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Add frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# MongoDB connection
client = MongoClient("mongodb+srv://shamsmohd:mlJ17DRDPZmuY9Kj@stocks.xscx2.mongodb.net/?retryWrites=true&w=majority&appName=stocks")
db = client["stock_data"]
collection = db["stocks"]

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Stock API",
        "endpoints": {
            "/fetch-stocks": "Fetch all stocks",
            "/filter-stocks": "Filter stocks based on parameters",
            "/sort-stocks": "Sort stocks by a parameter",
            "/stocks/{ticker}": "Get details for a specific stock",
        },
    }

@app.get("/search-stocks")
def search_stocks(query: str):
    """
    Search stocks by ticker or other fields.
    """
    search_query = {"$or": [
        {"ticker": {"$regex": query, "$options": "i"}},  # Case-insensitive match for ticker
        {"market_cap": {"$regex": query, "$options": "i"}},  # Optional: Search by market_cap as string
    ]}
    stocks = list(collection.find(search_query, {"_id": 0}))
    return {"stocks": stocks}


@app.get("/fetch-stocks")
def fetch_stocks(skip: int = 0, limit: int = 10):
    """
    Fetch all stock data from MongoDB with pagination.
    """
    try:
        stocks = list(collection.find({}, {"_id": 0}).skip(skip).limit(limit))
        return {"stocks": stocks}
    except Exception as e:
        return {"error": "Failed to fetch stocks", "details": str(e)}

@app.get("/filter-stocks")
def filter_stocks(
    market_cap_min: Optional[float] = Query(None, description="Minimum Market Cap"),
    market_cap_max: Optional[float] = Query(None, description="Maximum Market Cap"),
    pe_ratio_min: Optional[float] = Query(None, description="Minimum PE Ratio"),
    pe_ratio_max: Optional[float] = Query(None, description="Maximum PE Ratio"),
    debt_to_equity_min: Optional[float] = Query(None, description="Minimum Debt-to-Equity Ratio"),
    debt_to_equity_max: Optional[float] = Query(None, description="Maximum Debt-to-Equity Ratio"),
    eps_min: Optional[float] = Query(None, description="Minimum EPS"),
    eps_max: Optional[float] = Query(None, description="Maximum EPS"),
    dividend_yield_min: Optional[float] = Query(None, description="Minimum Dividend Yield"),
    dividend_yield_max: Optional[float] = Query(None, description="Maximum Dividend Yield"),
    return_on_equity_min: Optional[float] = Query(None, description="Minimum Return on Equity"),
    return_on_equity_max: Optional[float] = Query(None, description="Maximum Return on Equity"),
    price_to_book_min: Optional[float] = Query(None, description="Minimum Price-to-Book Ratio"),
    price_to_book_max: Optional[float] = Query(None, description="Maximum Price-to-Book Ratio"),
    current_ratio_min: Optional[float] = Query(None, description="Minimum Current Ratio"),
    current_ratio_max: Optional[float] = Query(None, description="Maximum Current Ratio"),
    operating_margin_min: Optional[float] = Query(None, description="Minimum Operating Margin"),
    operating_margin_max: Optional[float] = Query(None, description="Maximum Operating Margin"),
    net_profit_margin_min: Optional[float] = Query(None, description="Minimum Net Profit Margin"),
    net_profit_margin_max: Optional[float] = Query(None, description="Maximum Net Profit Margin"),
    free_cash_flow_min: Optional[float] = Query(None, description="Minimum Free Cash Flow"),
    free_cash_flow_max: Optional[float] = Query(None, description="Maximum Free Cash Flow"),
):
    """
    Filter stocks based on multiple parameters.
    """
    query = {}

    # Add filtering conditions for each parameter
    if market_cap_min is not None:
        query["market_cap"] = {"$gte": market_cap_min}
    if market_cap_max is not None:
        query["market_cap"] = query.get("market_cap", {})
        query["market_cap"]["$lte"] = market_cap_max

    if pe_ratio_min is not None:
        query["pe_ratio"] = {"$gte": pe_ratio_min}
    if pe_ratio_max is not None:
        query["pe_ratio"] = query.get("pe_ratio", {})
        query["pe_ratio"]["$lte"] = pe_ratio_max

    if debt_to_equity_min is not None:
        query["debt_to_equity_ratio"] = {"$gte": debt_to_equity_min}
    if debt_to_equity_max is not None:
        query["debt_to_equity_ratio"] = query.get("debt_to_equity_ratio", {})
        query["debt_to_equity_ratio"]["$lte"] = debt_to_equity_max

    if eps_min is not None:
        query["eps"] = {"$gte": eps_min}
    if eps_max is not None:
        query["eps"] = query.get("eps", {})
        query["eps"]["$lte"] = eps_max

    if dividend_yield_min is not None:
        query["dividend_yield"] = {"$gte": dividend_yield_min}
    if dividend_yield_max is not None:
        query["dividend_yield"] = query.get("dividend_yield", {})
        query["dividend_yield"]["$lte"] = dividend_yield_max

    if return_on_equity_min is not None:
        query["return_on_equity"] = {"$gte": return_on_equity_min}
    if return_on_equity_max is not None:
        query["return_on_equity"] = query.get("return_on_equity", {})
        query["return_on_equity"]["$lte"] = return_on_equity_max

    if price_to_book_min is not None:
        query["price_to_book_ratio"] = {"$gte": price_to_book_min}
    if price_to_book_max is not None:
        query["price_to_book_ratio"] = query.get("price_to_book_ratio", {})
        query["price_to_book_ratio"]["$lte"] = price_to_book_max

    if current_ratio_min is not None:
        query["current_ratio"] = {"$gte": current_ratio_min}
    if current_ratio_max is not None:
        query["current_ratio"] = query.get("current_ratio", {})
        query["current_ratio"]["$lte"] = current_ratio_max

    if operating_margin_min is not None:
        query["operating_margin"] = {"$gte": operating_margin_min}
    if operating_margin_max is not None:
        query["operating_margin"] = query.get("operating_margin", {})
        query["operating_margin"]["$lte"] = operating_margin_max

    if net_profit_margin_min is not None:
        query["net_profit_margin"] = {"$gte": net_profit_margin_min}
    if net_profit_margin_max is not None:
        query["net_profit_margin"] = query.get("net_profit_margin", {})
        query["net_profit_margin"]["$lte"] = net_profit_margin_max

    if free_cash_flow_min is not None:
        query["free_cash_flow"] = {"$gte": free_cash_flow_min}
    if free_cash_flow_max is not None:
        query["free_cash_flow"] = query.get("free_cash_flow", {})
        query["free_cash_flow"]["$lte"] = free_cash_flow_max

    try:
        stocks = list(collection.find(query, {"_id": 0}))
        return {"stocks": stocks}
    except Exception as e:
        return {"error": "Failed to filter stocks", "details": str(e)}

@app.get("/sort-stocks")
def sort_stocks(
    sort_by: str = Query(..., description="Parameter to sort by (e.g., pe_ratio, market_cap)"),
    order: str = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    """
    Sort stocks based on a parameter.
    """
    sort_order = 1 if order == "asc" else -1
    try:
        stocks = list(collection.find({}, {"_id": 0}).sort(sort_by, sort_order))
        return {"stocks": stocks}
    except Exception as e:
        return {"error": f"Invalid sort parameter: {sort_by}", "details": str(e)}

@app.get("/stocks/{ticker}")
def get_stock_by_ticker(ticker: str):
    """
    Fetch stock details by ticker.
    """
    try:
        stock = collection.find_one({"ticker": ticker}, {"_id": 0})
        if not stock:
            return {"error": f"Stock with ticker {ticker} not found"}
        return stock
    except Exception as e:
        return {"error": "Failed to fetch stock details", "details": str(e)}

@app.get("/get-historical-data/{ticker}")
def get_historical_data(ticker: str):
    """
    Get historical data for a specific stock.
    """
    try:
        stock = collection.find_one({"ticker": ticker}, {"_id": 0, "historical_data": 1})
        if not stock:
            return {"error": "Stock not found"}
        return stock
    except Exception as e:
        return {"error": "Failed to fetch historical data", "details": str(e)}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {"error": "An unexpected error occurred", "details": str(exc)}
