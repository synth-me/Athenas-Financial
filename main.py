from flask import Flask, render_template, request, jsonify
import Core 
from Core import Analysis, Engine, Scrapper 
import numpy as np
import textblob
from textblob import TextBlob
import time 
import json
import pandas as pd 

app = Flask(__name__)

# here we got the url for Quandl stock system that will lead to see the Trickers
# from the company’s name  
url = "https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/secwiki_tickers.csv"

@app.route("/main_sys",methods=["GET","POST"])
def search_main():
  # here its the only request needed 
  n_emp = request.args.get("nome_da_empresa")
  
  if n_emp != None:
    # here we start by loading the data from qunadl
    n_a = Analysis.search.database_func(url)
    # then we execute the main function from Analysis module 
    # it will return the stock informations 
    analyse = Analysis.search.company_values(n_emp,n_a,3)
    
    scores_key = {}
    scores_value = []
    not_values = []
    
    # here we filter the informations to let be jsonable 
    for an in analyse[0]:
      
      for ind in an.index:
        if ind in scores_key:
          pass
        else:
          scores_key[ind] = []
      
      for val in an :
        scores_value.append(val)
    
    zipped_values = list(zip(scores_value,scores_value))
    analyse_f = dict(zip(scores_key,zipped_values))
    
    # here will enter luiza’s code for scrapping
    # her code should return a variable of plain text called ‘text’ 
    # that plain text will be analysed by the main functon from Engine 
    # that will return a dictionary jsonable as the n_b example
    
    text_prime = Scrapper.wbscrp(n_emp)
    divided_text = (",".join(text_prime)).split(".")
    counter = len(divided_text) - 10
    while counter < len(divided_text):
      noticia = divided_text[counter]
      n_b = Engine.cluster_steps.compiled_functions(noticia) 
      not_values.append((counter,n_b))
      
      counter+=1
    
    print("passed analysis")
    print(analyse_f)
    print("passed values")
    print(not_values)
    
    # here its the response, the template is not needed actually 
    # the template is here for test purpose
    
    return render_template("Index.html",
    stock_info = jsonify(analyse_f),
    sent_info = jsonify(not_values)
    )
    
  else:
    return render_template("Index.html")
	

app.run(host='0.0.0.0', port=8080)

