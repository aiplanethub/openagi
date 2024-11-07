from typing import Any, Optional
from openagi.actions.base import ConfigurableAction
from openagi.exception import OpenAGIException
from pydantic import Field

try:
	import yfinance as yf
except ImportError:
	raise OpenAGIException("Install yfinance with cmd `pip install yfinance`")

class YahooFinanceTool(ConfigurableAction):
	"""Yahoo Finance tool for fetching stock market data.
	
	This action uses the yfinance library to retrieve financial information
	about stocks, including current price, historical data, and company info.
	"""
	
	symbol: str = Field(..., description="Stock symbol to look up (e.g., 'AAPL' for Apple)")
	info_type: str = Field(
		default="summary",
		description="Type of information to retrieve: 'summary', 'price', 'history', or 'info'"
	)
	period: Optional[str] = Field(
		default="1d",
		description="Time period for historical data (e.g., '1d', '5d', '1mo', '1y')"
	)

	def execute(self) -> str:
		try:
			stock = yf.Ticker(self.symbol)
			
			if self.info_type == "summary":
				info = stock.info
				return (
					f"Company: {info.get('longName', 'N/A')}\n"
					f"Current Price: ${info.get('currentPrice', 'N/A')}\n"
					f"Market Cap: ${info.get('marketCap', 'N/A')}\n"
					f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}\n"
					f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}"
				)
				
			elif self.info_type == "price":
				return f"Current price of {self.symbol}: ${stock.info.get('currentPrice', 'N/A')}"
				
			elif self.info_type == "history":
				history = stock.history(period=self.period)
				if history.empty:
					return f"No historical data available for {self.symbol}"
				
				latest = history.iloc[-1]
				return (
					f"Historical data for {self.symbol} (last entry):\n"
					f"Date: {latest.name.date()}\n"
					f"Open: ${latest['Open']:.2f}\n"
					f"High: ${latest['High']:.2f}\n"
					f"Low: ${latest['Low']:.2f}\n"
					f"Close: ${latest['Close']:.2f}\n"
					f"Volume: {latest['Volume']}"
				)
				
			elif self.info_type == "info":
				info = stock.info
				return (
					f"Company Information for {self.symbol}:\n"
					f"Industry: {info.get('industry', 'N/A')}\n"
					f"Sector: {info.get('sector', 'N/A')}\n"
					f"Website: {info.get('website', 'N/A')}\n"
					f"Description: {info.get('longBusinessSummary', 'N/A')}"
				)
				
			else:
				return f"Invalid info_type: {self.info_type}. Supported types are: summary, price, history, info"
				
		except Exception as e:
			return f"Error fetching data for {self.symbol}: {str(e)}"