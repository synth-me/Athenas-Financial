# aqui vao os arquivos relativos a analise
# das noticias 
from googletrans import Translator 
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import floresta 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from textblob import TextBlob
from textblob import Word 
from textblob.wordnet import Synset
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pycountry
import re
import numpy as np
import math

#nltk.download('all')

#———————————————————-#

class cluster_steps():

# here the language is spotted

  def lang_tracker(sentence):
    
    f_language = []
    
    sentence_blob = TextBlob(sentence)
    try:
      abb_lang = sentence_blob.detect_language()
      p_language = pycountry.languages.get(alpha_2=abb_lang)
      v_language = (p_language.name).lower()
      f_language.append(v_language)
    except:
      f_language.append("english")
    
    return f_language
  
  def stopwords_spot(text):
    
    text_filtered = []
    
    for sentence in text.split("."):
      
      for sent in sent_tokenize(sentence):
        
        if len(sent) > 3:
          
          lng = cluster_steps.lang_tracker(sent)
          stop = stopwords.words(lng)
        else:
          stop = stopwords.word("english")
        
      for word in word_tokenize(sentence):
        
        if word in stop :
          pass
        else:
          text_filtered.append(word)
        
        
    return text_filtered
  
  def domain(text):
    translator = Translator()
    #nltk.download('all')
    
    stop_detected = []
    text_filtered = []
    information_text = []
    
    text_filtered = cluster_steps.stopwords_spot(text)
    for word in text_filtered:
      
      n = nltk.tag.pos_tag([translator.translate(word).text])
      information_text.append(n)
      
    return information_text
    
  def classification(information_text):
    
    #nltk.download('all')
    
    noun_list = []
    max_list = []

# here we select only the nouns and adjectives 
    
    for information in information_text:
      for info in information:
        t_N = re.findall("^N",info[1])
        t_V = re.findall("^J",info[1])
        if t_N or t_V :
          noun_list.append(info[0])
        
    return noun_list
  
  
  def tf_idf(text,noun_verbs):
    
    tf_idf_data = {}
    
    txtf = cluster_steps.stopwords_spot(text)
    length_text = len(text.split())
    
    for word in noun_verbs :
      
      try:
        ct = (text.split()).count(word)
        tf_idf_data[word] = ct*math.log(length_text/ct) 
      except:
        pass
      
    return tf_idf_data  
  
  
  def sentiment_analysis_0(noun_verbs):
    
    sentiment_dict = {}
    for word in noun_verbs:
      try:
        word_t = TextBlob(word)
        w = word_t.sentiment
        sentiment_dict[word] = (w.polarity,w.subjectivity)
      except:
        sentiment_dict[word] = (0.0,0.0)
      
    return sentiment_dict 
  
  def sentiment_analysis_1(noun_verbs):
    
    analyzer = SentimentIntensityAnalyzer()
    
    sentiment_dict = {}
    
    for word in noun_verbs :
      
      intensity = analyzer.polarity_scores(word)
      
      sentiment_dict[word] = intensity["compound"] 
      
    return sentiment_dict
  
  def my_model(tf_idf_data,sentiment_dict):
    
    processed_data = {}
    
    weight_sub_value = []
    weight_pol_value = []
    
    desv_pol_list = []
    desv_sub_list = [] 
    
    for word in sentiment_dict:
      
      if word in tf_idf_data:
        sigma = tf_idf_data[word]
        sentiment = sentiment_dict[word]
        w_sentiment = round(sentiment[0]/(1+sigma),2)
        w_subjectivity = round(sentiment[1]/(1+sigma),2)
        
        processed_data[word] = (w_sentiment,w_subjectivity)
    
    for v_words in processed_data:
      
      weight_sub_value.append(processed_data[v_words][1])
      weight_pol_value.append(processed_data[v_words][0])
    
    final_pol = sum(weight_sub_value)/(1+len(weight_sub_value))
    final_sub = sum(weight_pol_value)/(1+len(weight_pol_value))
    
    for values_pol in weight_pol_value:
      desv_pol = final_pol - values_pol 
      if desv_pol >= 0:
        desv_pol_list.append(desv_pol)
      else:
        desv_pol_list.append(desv_pol*-1)
    
    trust_pol = sum(desv_pol_list)/(1+len(desv_pol_list))
    
    for values_sub in weight_sub_value:
      desv_sub = final_sub - values_sub 
      if desv_sub >= 0:
        desv_sub_list.append(desv_sub)
      else:
        desv_sub_list.append(desv_sub*-1)
    
    trust_sub = sum(desv_sub_list)/(1+len(desv_sub_list))
    
    return {"Final polarity":(round(final_pol,2),round(trust_pol,2)),"Final subjectivity":(round(final_sub,2),round(trust_sub,2))}
  
  
  def compiled_functions(text_use,sent=0):
    
    a = cluster_steps.lang_tracker(text_use)
    b = cluster_steps.domain(text_use)
    c = cluster_steps.classification(b)
    if sent == 1 :
      d = cluster_steps.sentiment_analysis_1(c)
    else:
      d = cluster_steps.sentiment_analysis_0(c)
    e = cluster_steps.tf_idf(text_use,c)
    f = cluster_steps.my_model(e,d)
    return f 
  