import yfinance as ys 
import datetime 
import quandl 
import requests 
import io 
import pandas as pd 
from difflib import SequenceMatcher

url = "https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/secwiki_tickers.csv"

s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))
data_c = pd.DataFrame(c)
database = data_c.set_index("Name")

class search():
  
  def database_func(url):
    s = requests.get(url).content
    s = pd.read_csv(io.StringIO(s.decode("utf-8")))
    data_c = pd.DataFrame(c)
    database = data_c.set_index("Name")
    return database
    
  def company_search(company,range=1):
    
    total_values = []
    
    n = ys.Ticker(company)
    n_1 = n.history()
    
    counter = 1 
    while counter <= range :
      
      a = n_1.iloc[len(n_1)-counter]
      total_values.append(a)
      
      counter+=1
      
    return total_values 

  def similarity(company,database):
    
    sm = {}
      
    counter = 0
    while counter < len(database):
      
      
      data_prime = database.iloc[counter]
      data = data_prime.name
      data_1 = data_prime["Ticker"]
      
      s = SequenceMatcher(None,company,str(data)).ratio()
      sm[s] = (data,data_1) 
      
      counter+=1 

    try:
      mk = max(sm.keys())
      return sm[mk]
    except:
      return "ta ta ta ja entendi"
    
    #s = SequenceMatcher(None,company,company_target).ratio()

  def company_values(company,database,range=1):
    
    a = search.similarity(company,database)
    b = search.company_search(a[1],range)
    
    return (b,a[0]) 
