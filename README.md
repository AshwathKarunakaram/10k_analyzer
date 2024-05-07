# 10k_analyzer
Sentiment Analysis and Stock Price Visualization

Short Demo: https://youtu.be/Xf3764Lb5lo

# Overview
This project aims to provide sentiment analysis on the Management's Discussion and Analysis (MD&A) section extracted from the SEC filings (Form 10-K) of two companies, Apple Inc. (AAPL) and NVIDIA Corporation (NVDA), spanning from 1995 to 2023. I used the MD&A section specifically because it represents the persepective of the company's management. Additionally, it visualizes the sentiment trends over time and correlates them with the respective companies' stock prices. 

# Tech Stack
Python is chosen as the programming language due to its versatility, extensive libraries for data analysis, natural language processing (NLP), and data visualization.

# Libraries Used

<ins>edgartools</ins>

Purpose: Used for scraping SEC filings from the EDGAR database. The edgar library simplifies the process of fetching Form 10-K filings, making it convenient for data acquisition.

<ins>langchain_community</ins>

Purpose: Utilizes the LLM (Long Language Model) to assess sentiment in the MD&A section of the 10-k form. The llms module offers an LLM (llama2) model to evaluate the sentiment of text segments. This choice ensures robust sentiment analysis.

<ins>sumy</ins>

Purpose: Performs text summarization. Summarization using the TextRank algorithm helps to condense lengthy MD&A sections for efficient sentiment analysis.

<ins>pandas</ins>

Purpose: Provides data manipulation and analysis capabilities. This is used extensively for handling dataframes and CSV files, enabling efficient data processing.

<ins>plotly</ins>

Purpose: Generates interactive visualizations.
Explanation: plotly is employed to create dynamic and visually appealing charts for sentiment trends and stock price analysis.

<ins>yfinance</ins>

Purpose: Retrieves historical stock price data.
Explanation: yfinance facilitates the retrieval of historical stock prices, which is essential for visualizing stock price trends.

<ins>panel</ins>

Purpose: Creates interactive web applications. Leveraged to develop a simple and interactive dashboard for displaying sentiment analysis and stock price visualizations.

# Challenges
Time: The LLM took a long time to process the text and sometimes it responded with invalid data. This problem was solved with engineering better and more specific prompts, and condensing the text as much as possible.

# License
This project is licensed under the MIT License.

# Acknowledgements
The project utilizes data from the SEC EDGAR database and Yahoo Finance.
