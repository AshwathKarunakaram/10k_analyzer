# Ashwath Karunakaram
# 5/7/24
# DARPA Research App Submission
# Backend to scrape data, clean data, process data with LLM, create graphs

from edgar import set_identity
from edgar.financials import *
import pandas as pd
from edgar import Company
import csv
import re  
from langchain_community.llms import Ollama
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import pandas as pd
import plotly.express as px
import csv
import yfinance as yf


llm = Ollama(model="llama2") # LLM Model llama2

sentiments_list_aapl = {}
sentiments_list_nvda = {}

#--------------------------------------------------------------------------
# Function to get company's filings from 1995-2024
# Uses EdgarTools
# Takes in company object and year
# Returns filings
#--------------------------------------------------------------------------
def get_data(company, year):  # API call with Edgartools get_filings
    return company.get_filings(form="10-K").filter(date=f"{year}-01-01:{year+1}-03-01")

#--------------------------------------------------------------------------
# Function to download only Item 7 from each filing as csv
# Uses regex, csv
# Takes in company name and company object
# Returns nothing
#--------------------------------------------------------------------------

def download_10k_filings_as_csv(compString, company): # initial data scrapping and cleaning with regex
    with open(f'{compString}.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(["Year", "7: MD&A"])
        for i in range(1995, 2024):
            try:
                tenk = get_data(company, i)[0] 
                tenobj = tenk.obj()

                pattern = r'(?:\b[Ii]tem 7\.?|\|)(.*)' # regex pattern
                md_a_match = re.search(pattern, tenobj["Item 7"], re.DOTALL) # search text for regex pattern and delete occurences
                md_a_text = md_a_match.group(1).strip() if md_a_match else tenobj["Item 7"]
                md_a_text = md_a_text.replace('\n', '').lstrip() # strip leading characters

                writer.writerow([i, md_a_text]) # write cleaned text into csv file
            except AttributeError:
                print(f"{i} is skipped")
            except TypeError:
                print(f"{i} is skipped") # error handling

#--------------------------------------------------------------------------
# Function to summarize text since LLM cannot process large text properly
# Uses sumy
# Takes in input text
# Returns summarized text
#--------------------------------------------------------------------------
def summarize_text(input):
    parser = PlaintextParser.from_string(input, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences_count=10) # Gets maximum 10 sentences
    summary_list = {}
    for sentence in summary:
        if "|" not in str(sentence):
            summary_list[str(sentence)] = None
    return summary_list


#--------------------------------------------------------------------------
# Function to generate sentiment for each year's Item 7 section and write to csv
# Uses regex, llm llama2
# Takes in company name, dataframe, listSentiments
# Returns nothing
#--------------------------------------------------------------------------

def generate_sentiments(comp, df, listSentiments):
    with open(f'{comp}_result.txt', 'w') as f:
            
        for i in range (0, len(df)):
            sentences_ratings = summarize_text(df.get("7: MD&A")[i]) # Summarizes Item 7 
            year = df.get("Year")[i]
            if(len(sentences_ratings) > 0):
                for s in sentences_ratings:
                    response = llm.invoke("Assess the sentiment of the following sentence solely based on its impact on the company's welfare. Disregard any external factors or the tone of the sentence. Provide a sentiment score within the range of -1 to 1, where -1 represents a negative sentiment, 0 is neutral, and 1 indicates a positive sentiment. Decimals are acceptable for nuanced scoring. You must give a number in your response in the desired range mentioned previously. Here's an example sentence: 'To the extent the Company's financial losses in prior years and the minority market share held by the Company in the personal computer market, as well as the Company's decision to end its Mac OS licensing program, have caused software developers to question the Company's prospects in the personal computer market, developers could be less inclined to develop new application software or upgrade existing software for the Company's products and more inclined to devote their resources to developing and upgrading software for the larger Windows market.' Another example, the following sentence would have positive score from 0 to 1 since some losses from the previous year are being offset: These losses in 2002 were partially offset by the sale of 117,000 shares of EarthLink stock for net proceeds of $2 million and a gain before taxes of $223,000, the sale of 250,000 shares of Akamai stock for net proceeds of $2 million and a gain before taxes of $710,000, and the sale of approximately 4.7 million shares of ARM stock for both net proceeds and a gain before taxes of $21 million. Provide a sentiment score based on the sentence's impact on the company's welfare. " + ", ".join(s))
                    print(response + ": " + s + "\n")
                    pattern = r"[-+]?\d*\.?\d+" 
                    first_number_match = re.search(pattern, response) # gets the number in the response as sentiment score
                    if(first_number_match is not None):
                        first_number_str = first_number_match.group()
                        first_number = float(first_number_str)
                    else:
                        first_number = 0
                    sentences_ratings[s] = first_number


                avgRating = sum(sentences_ratings.values()) / len(sentences_ratings) # averages sentiment for all sentences
                listSentiments[year] = avgRating
                f.write(f"{year},{avgRating}\n") # writes sentiment score for that year

#--------------------------------------------------------------------------
# Function to convert text into csv
# Uses csv
# Takes in company string
# Returns nothing
#--------------------------------------------------------------------------

def convert_txt(comp):
    with open(f'{comp}_result.txt', 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open(f'{comp}_result.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(('Year', 'S-Score'))
            writer.writerows(lines)

#--------------------------------------------------------------------------
# Function to make sentiment score chart 
# Uses plotly
# Takes in filepath of csv
# Returns graph
#--------------------------------------------------------------------------

def make_yearly_line_chart(comp):
    df = pd.read_csv(comp)
    fig = px.line(df, x = 'Year', y = 'S-Score', title='S-Score of SEC Filing Over Time (1995-2023)')
    return fig

#--------------------------------------------------------------------------
# Function to make stock chart 
# Uses yfinance and plotly
# Takes in filepath of csv
# Returns graph
#--------------------------------------------------------------------------

def make_yearly_stock_chart(comp):
    df = pd.read_csv(comp)
    fig = px.line(df, x = 'Date', y = 'Close', title='Open Stock Price Over Time (1995-2023)')
    return fig

#--------------------------------------------------------------------------
# Main method, provides framework
#--------------------------------------------------------------------------

def main():
    set_identity("AK ak@gmail.com")
    aapl = Company("AAPL")
    nvda = Company("NVDA")

    download_10k_filings_as_csv("aapl", aapl) # comment out after initial download
    download_10k_filings_as_csv("nvda", nvda) # comment out after initial download

    aapldf = pd.read_csv('aapl.csv') # comment out after initial download
    nvdadf = pd.read_csv('nvda.csv') # comment out after initial download

    generate_sentiments("apple", aapldf, sentiments_list_aapl) # comment out after initial analysis
    generate_sentiments("nvidia", nvdadf, sentiments_list_nvda) # comment out after initial download

    convert_txt("apple") 
    convert_txt("nvidia")
    start_date = '2002-01-01'
    end_date = '2023-01-01'

    # Download the stock data from Yahoo Finance
    data_aapl = yf.download("AAPL", start=start_date, end=end_date) # comment out after initial download
    data_nvda = yf.download("NVDA", start=start_date, end=end_date) # comment out after initial download

    # Save data to csv files containing only 'Date' and 'Open' columns
    data_aapl[['Close']].reset_index().to_csv('aapl_data.csv', index=False)
    data_nvda[['Close']].reset_index().to_csv('nvda_data.csv', index=False)

    
    aapl_line_sscore = make_yearly_line_chart("apple_result.csv")
    nvda_line_sscore = make_yearly_line_chart("nvidia_result.csv")
    aapl_line_stock = make_yearly_stock_chart("aapl_data.csv")
    nvda_line_stock = make_yearly_stock_chart("nvda_data.csv")
    return aapl_line_sscore, nvda_line_sscore, aapl_line_stock, nvda_line_stock
    
# Returns graphs to program that imports
if __name__ == "__main__":
    aapl_line_sscore, nvda_line_sscore, aapl_line_stock, nvda_line_stock = main()