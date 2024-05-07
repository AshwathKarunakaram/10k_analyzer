# 10k_analyzer
Sentiment Analysis and Stock Price Visualization
# Overview
This project aims to provide sentiment analysis on the Management's Discussion and Analysis (MD&A) section extracted from the SEC filings (Form 10-K) of two companies, Apple Inc. (AAPL) and NVIDIA Corporation (NVDA), spanning from 1995 to 2023. Additionally, it visualizes the sentiment trends over time and correlates them with the respective companies' stock prices.

# Tech Stack
Python
Python is chosen as the primary programming language due to its versatility, extensive libraries for data analysis, natural language processing (NLP), and visualization.

# Libraries Used

edgar
Purpose: Used for scraping SEC filings from the EDGAR database.
Explanation: The edgar library simplifies the process of fetching Form 10-K filings, making it convenient for data acquisition.

langchain_community
Purpose: Utilizes the LLM (Long Language Model) to assess sentiment in the MD&A section.
Explanation: The llms module offers an LLM (llama2) model to evaluate the sentiment of text segments. This choice ensures robust sentiment analysis.

sumy
Purpose: Performs text summarization.
Explanation: Summarization using the TextRank algorithm helps to condense lengthy MD&A sections for efficient sentiment analysis.

pandas
Purpose: Provides data manipulation and analysis capabilities.
Explanation: Used extensively for handling dataframes and CSV files, enabling efficient data processing.

plotly
Purpose: Generates interactive visualizations.
Explanation: plotly is employed to create dynamic and visually appealing charts for sentiment trends and stock price analysis.

yfinance
Purpose: Retrieves historical stock price data.
Explanation: yfinance facilitates the retrieval of historical stock prices, which is essential for visualizing stock price trends.

panel
Purpose: Creates interactive web applications.
Explanation: Leveraged to develop an interactive dashboard for displaying sentiment analysis and stock price visualizations.

# License
This project is licensed under the MIT License.

# Acknowledgements
The project utilizes data from the SEC EDGAR database and Yahoo Finance.
