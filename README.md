Stock Filtering and Analysis Application
Overview
This project is a backend solution for fetching, processing, storing, and analyzing stock data. It utilizes:

Yahoo Finance for gathering historical and financial stock data.
MongoDB for storing and managing the stock information.
FastAPI for providing RESTful endpoints to fetch, filter, and sort stock data dynamically.
The application supports operations like:

Fetching data for 25 Indian stocks.
Storing stock data in MongoDB with additional financial parameters.
Filtering and sorting stock data using parameters like PE Ratio, Market Cap, and more.
Features
Download Stock Data:
Fetch historical stock data for specified tickers using Yahoo Finance.
Store Data in MongoDB:
Store stock data with additional financial metrics (e.g., PE Ratio, EPS) into a MongoDB database.
RESTful API:
Filter, search, and sort stocks via FastAPI endpoints.
Data Validation:
Ensure data accuracy by cleaning and validating input CSV files.
Project Structure
graphql
Copy code
backend/
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── stockdata.py           # Script to fetch and save historical stock data
│   ├── app.py                 # FastAPI routes for filtering, sorting, and searching stocks
│   └── store_to_mongodb.py    # Script to store stock data into MongoDB with financial parameters
└── requirements.txt           # Dependency list
Setup and Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/stock-filtering-app.git
cd stock-filtering-app/backend
2. Install Dependencies
Create a Python virtual environment (optional but recommended) and install the dependencies:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows, use env\Scripts\activate
pip install -r requirements.txt
Dependencies include:

fastapi
uvicorn
pymongo
yfinance
pandas
3. Set Up MongoDB
Local MongoDB:
Install MongoDB and start the database server.
Update the MONGO_URI in store_to_mongodb.py and app.py with mongodb://localhost:27017.
MongoDB Atlas:
Sign up for a MongoDB Atlas account.
Create a cluster, whitelist your IP address, and get the connection string.
Update the MONGO_URI in store_to_mongodb.py and app.py with your connection string.
Usage
1. Fetch and Save Historical Stock Data
Run the stockdata.py script to fetch historical data for 25 Indian stocks and save them as CSV files in a stock_data folder:

bash
Copy code
python app/stockdata.py
The script:

Fetches data for 25 predefined Indian stock tickers.
Saves each stock's historical data as a CSV file in the stock_data directory.
2. Store Data in MongoDB
Run the store_to_mongodb.py script to:

Read the CSV files from the stock_data folder.
Fetch additional financial data (e.g., PE Ratio, EPS) using Yahoo Finance.
Store the processed data into the MongoDB database.
bash
Copy code
python app/store_to_mongodb.py
3. Start the FastAPI Server
Run the FastAPI app:

bash
Copy code
uvicorn app.app:app --reload
The server will start at: http://127.0.0.1:8000.

4. API Endpoints
Base URL: http://127.0.0.1:8000

Returns a welcome message and a list of available endpoints.
Fetch All Stocks: /fetch-stocks

Fetch all stock data with optional pagination (skip, limit).
Search Stocks: /search-stocks

Search stocks by ticker or other fields.
Filter Stocks: /filter-stocks

Filter stocks based on parameters like:
Market Cap
PE Ratio
EPS
Debt-to-Equity, etc.
Sort Stocks: /sort-stocks

Sort stocks by any parameter (e.g., PE Ratio, Market Cap) in ascending/descending order.
Stock Details by Ticker: /stocks/{ticker}

Get detailed information for a specific stock by ticker symbol.
Historical Data by Ticker: /get-historical-data/{ticker}

Get historical data for a specific stock by ticker symbol.
Example Requests
Fetch All Stocks
bash
Copy code
GET http://127.0.0.1:8000/fetch-stocks
Filter Stocks by Market Cap
bash
Copy code
GET http://127.0.0.1:8000/filter-stocks?market_cap_min=1000000000&market_cap_max=5000000000
Sort Stocks by PE Ratio
bash
Copy code
GET http://127.0.0.1:8000/sort-stocks?sort_by=pe_ratio&order=desc
Search for a Stock by Ticker
bash
Copy code
GET http://127.0.0.1:8000/search-stocks?query=RELIANCE

Stock Filtering and Analysis Dashboard (Frontend)
Overview
This project is the frontend application for a Stock Filtering and Analysis Dashboard. Built with React.js, it provides an interactive interface to:

Display stock data in a table.
Search, filter, and sort stocks based on financial parameters like PE Ratio, Market Cap, etc.
Paginate through the stock list for easy navigation.
The frontend communicates with a FastAPI backend to fetch stock data stored in a MongoDB database.

Features
Dynamic Search: Search stocks by ticker or other criteria.
Sorting: Sort stocks dynamically by any parameter (e.g., Market Cap, PE Ratio).
Filtering: Apply filters for specific financial metrics (e.g., minimum/maximum PE Ratio, Market Cap).
Pagination: Navigate through large datasets with pagination.
Responsive Design: Ensures usability across different devices.
Project Structure
php
frontend/
├── public/                     # Static assets like images and favicon
│   ├── 6256878.jpg             # Background image
│   └── index.html              # HTML entry point
├── src/                        # React application code
│   ├── App.js                  # Main React component
│   ├── App.css                 # Styling for the app
│   └── index.js                # React DOM rendering
├── package.json                # Project metadata and dependencies
└── README.md                   # Documentation
Setup and Installation
1. Clone the Repository
bash
git clone https://github.com/yourusername/stock-filtering-dashboard.git
cd stock-filtering-dashboard/frontend
2. Install Dependencies
Install all required dependencies using npm:

bash
npm install
3. Update Backend URL
Open App.js.
Update the API_BASE_URL variable with your backend URL:
javascript
Copy code
const API_BASE_URL = "http://localhost:8000"; // Replace with your backend URL
How to Run the Project
Start the Development Server
Run the following command to start the React development server:

bash
npm start

The application will be accessible at http://localhost:3000.
Ensure that your backend (FastAPI) is running at the URL specified in API_BASE_URL.
Key Functionalities
1. Search Stocks
Enter a stock ticker or keyword in the search bar.
Click "Search" to filter results based on your input.
2. Sorting Stocks
Select a parameter (e.g., PE Ratio, Market Cap) in the "Sort By" dropdown.
Choose sorting order (Ascending or Descending).
Click "Apply Sorting" to sort the table.
3. Filtering Stocks
Enter minimum and maximum values for parameters like PE Ratio or Market Cap.
Click "Apply Filters" to filter the stock list.
4. Pagination
Navigate between pages using the pagination bar at the bottom of the page.
Styling
Theme
The application has a professional and minimalistic design:

Background: A stock market-themed image for a modern look.
Components: Styled using Material-UI with customizations in App.css.
Custom CSS
App.css defines the overall page layout, including:
A transparent container for readability.
Styled buttons, inputs, and tables for better user experience.
Example Screenshots
Dashboard
A snapshot of the stock dashboard with table, filters, and pagination (add screenshots for better representation).

Key Dependencies
React: Frontend framework.
Axios: For API requests.
Material-UI: Component library for UI elements.
To install dependencies manually:

bash
npm install react axios @mui/material @mui/icons-material
