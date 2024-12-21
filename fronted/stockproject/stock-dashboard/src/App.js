import React, { useState, useEffect } from "react";
import axios from "axios";
import './App.css';
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  Button,
  Select,
  MenuItem,
  CircularProgress,
  Grid,
  Pagination,
} from "@mui/material";

const API_BASE_URL = "http://localhost:8000"; // Replace with your backend URL

function App() {
  const [stocks, setStocks] = useState([]);
  const [searchQuery, setSearchQuery] = useState(""); // Search functionality
  const [sortBy, setSortBy] = useState(""); // Sorting parameter
  const [sortOrder, setSortOrder] = useState("asc"); // Sorting order
  const [filterParams, setFilterParams] = useState({
    pe_ratio_min: "",
    pe_ratio_max: "",
    market_cap_min: "",
    market_cap_max: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10; // Show 10 items per page

  // Fetch all stocks
  const fetchStocks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/fetch-stocks`);
      setStocks(response.data.stocks || []);
    } catch (err) {
      console.error("Error fetching stocks:", err);
      setError("Failed to fetch stocks. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  // Handle search
  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/search-stocks`, {
        params: { query: searchQuery },
      });
      setStocks(response.data.stocks || []);
    } catch (err) {
      console.error("Error during search:", err);
      setError("Failed to perform search.");
    } finally {
      setLoading(false);
    }
  };

  // Apply sorting
  const applySorting = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/sort-stocks`, {
        params: { sort_by: sortBy, order: sortOrder },
      });
      setStocks(response.data.stocks || []);
    } catch (err) {
      console.error("Error applying sorting:", err);
      setError("Failed to apply sorting.");
    } finally {
      setLoading(false);
    }
  };

  // Apply filtering
  const applyFiltering = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/filter-stocks`, {
        params: filterParams,
      });
      setStocks(response.data.stocks || []);
    } catch (err) {
      console.error("Error applying filters:", err);
      setError("Failed to apply filters.");
    } finally {
      setLoading(false);
    }
  };

  // Handle filter input changes
  const handleFilterChange = (e) => {
    setFilterParams({ ...filterParams, [e.target.name]: e.target.value });
  };

  // Handle pagination
  const handlePageChange = (event, value) => {
    setCurrentPage(value);
  };

  // Fetch stocks on mount
  useEffect(() => {
    fetchStocks();
  }, []);

  // Paginate stocks
  const paginatedStocks = stocks.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <Container>
      <h1>Stock Dashboard</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {loading && <CircularProgress style={{ marginBottom: "20px" }} />}

      {/* Search */}
      <Grid container spacing={2} style={{ marginBottom: "20px" }}>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Search by Ticker"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleSearch}
          >
            Search
          </Button>
        </Grid>
      </Grid>

      {/* Sorting */}
      <Grid container spacing={2} style={{ marginBottom: "20px" }}>
        <Grid item xs={6} sm={4}>
          <Select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            displayEmpty
            fullWidth
          >
            <MenuItem value="">Sort By</MenuItem>
            <MenuItem value="market_cap">Market Cap</MenuItem>
            <MenuItem value="pe_ratio">PE Ratio</MenuItem>
            <MenuItem value="debt_to_equity_ratio">Debt-to-Equity Ratio</MenuItem>
            <MenuItem value="eps">EPS</MenuItem>
            <MenuItem value="dividend_yield">Dividend Yield</MenuItem>
            <MenuItem value="return_on_equity">Return on Equity</MenuItem>
            <MenuItem value="price_to_book_ratio">Price-to-Book Ratio</MenuItem>
            <MenuItem value="current_ratio">Current Ratio</MenuItem>
            <MenuItem value="operating_margin">Operating Margin</MenuItem>
            <MenuItem value="net_profit_margin">Net Profit Margin</MenuItem>
            <MenuItem value="free_cash_flow">Free Cash Flow</MenuItem>
          </Select>
        </Grid>
        <Grid item xs={6} sm={4}>
          <Select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            fullWidth
          >
            <MenuItem value="asc">Ascending</MenuItem>
            <MenuItem value="desc">Descending</MenuItem>
          </Select>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={applySorting}
          >
            Apply Sorting
          </Button>
        </Grid>
      </Grid>

      {/* Filtering */}
      <Grid container spacing={2} style={{ marginBottom: "20px" }}>
        <Grid item xs={6}>
          <TextField
            label="Min PE Ratio"
            name="pe_ratio_min"
            value={filterParams.pe_ratio_min}
            onChange={handleFilterChange}
            fullWidth
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            label="Max PE Ratio"
            name="pe_ratio_max"
            value={filterParams.pe_ratio_max}
            onChange={handleFilterChange}
            fullWidth
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            label="Min Market Cap"
            name="market_cap_min"
            value={filterParams.market_cap_min}
            onChange={handleFilterChange}
            fullWidth
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            label="Max Market Cap"
            name="market_cap_max"
            value={filterParams.market_cap_max}
            onChange={handleFilterChange}
            fullWidth
          />
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={applyFiltering}
          >
            Apply Filters
          </Button>
        </Grid>
      </Grid>

      {/* Stock Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ticker</TableCell>
              <TableCell>Market Cap</TableCell>
              <TableCell>PE Ratio</TableCell>
              <TableCell>Debt-to-Equity</TableCell>
              <TableCell>EPS</TableCell>
              <TableCell>Dividend Yield</TableCell>
              <TableCell>Return on Equity</TableCell>
              <TableCell>Price-to-Book Ratio</TableCell>
              <TableCell>Current Ratio</TableCell>
              <TableCell>Operating Margin</TableCell>
              <TableCell>Net Profit Margin</TableCell>
              <TableCell>Free Cash Flow</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedStocks.map((stock) => (
              <TableRow key={stock.ticker}>
                <TableCell>{stock.ticker}</TableCell>
                <TableCell>{stock.market_cap}</TableCell>
                <TableCell>{stock.pe_ratio}</TableCell>
                <TableCell>{stock.debt_to_equity_ratio}</TableCell>
                <TableCell>{stock.eps}</TableCell>
                <TableCell>{stock.dividend_yield}</TableCell>
                <TableCell>{stock.return_on_equity}</TableCell>
                <TableCell>{stock.price_to_book_ratio}</TableCell>
                <TableCell>{stock.current_ratio}</TableCell>
                <TableCell>{stock.operating_margin}</TableCell>
                <TableCell>{stock.net_profit_margin}</TableCell>
                <TableCell>{stock.free_cash_flow}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Pagination */}
      <Grid container justifyContent="center" style={{ marginTop: "20px" }}>
        <Pagination
          count={Math.ceil(stocks.length / itemsPerPage)}
          page={currentPage}
          onChange={handlePageChange}
          color="primary"
        />
      </Grid>
    </Container>
  );
}

export default App;
