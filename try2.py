import streamlit as st
import time
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from bs4 import BeautifulSoup
import requests

def getSentiment(bankName):
  bank_name = bankName
  article_info = []
  search_url = f"https://www.google.com/search?q={bank_name}&sxsrf=APwXEdfVzpfAF54BQQ6e0mr5fI2tPeW97A:1680341954287&source=lnms&tbm=nws&sa=X&ved=2ahUKEwie8KTKsYj-AhWkU2wGHatNBAkQ_AUoAnoECAEQBA&biw=1536&bih=754&dpr=1.25"
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
  }
  response = requests.get(search_url, headers=headers)
  soup = BeautifulSoup(response.content, "lxml")

  article_links = []
  links = soup.find_all("a")
  for tag in links:
      href = tag.get("href")
      if href.startswith('/url?esrc=s&q=&rct=j&sa=U&url=')==True:
        index = href.find("&ved=")
        if index != -1:
            href = href[:index]
        article_links.append(href[30::])

  article_data = []
  article_title = []

  for link in article_links:
    response_ = requests.get(link, headers=headers)
    soup_ = BeautifulSoup(response_.content, "lxml")
    title = soup_.find("title")
    article_title.append(title.text)  
    meta_tag = soup_.find('meta', attrs={'name': 'description'})
    if meta_tag:
      description = meta_tag.get('content')
      article_data.append(description)
      print(description)

  finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
  tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
  nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

  article_info = []  
  for description, url, title in zip(article_data, article_links, article_title):
        results = nlp(description)
        article_info.append({"URL": url, "Sentiment": results[0], "Title": title})

  return article_info

# Streamlit App
st.title("Stock News Sentiment Analyzer")
bank_name = st.text_input("Enter a Stock Name:", "HDFC")

if st.button("Analyze Sentiment"):
    with st.spinner("Analyzing news articles..."):
        results = getSentiment(bank_name)

    st.subheader("Results:")
    for article in results:
        st.write(f"**Title:** {article['Title']}")
        st.write(f"**URL:** {article['URL']}")
        st.write(f"**Sentiment:** {article['Sentiment']['label']}, Score: {article['Sentiment']['score']:.3f}")
        st.write("----") 











# import streamlit as st
# import time
# from transformers import BertTokenizer, BertForSequenceClassification, pipeline
# from bs4 import BeautifulSoup
# import requests

# def getSentiment(bankName):
#   # Search and scrape news articles
#   search_url = f"https://www.google.com/search?q={bankName}&sxsrf=APwXEdfVzpfAF54BQQ6e0mr5fI2tPeW97A:1680341954287&source=lnms&tbm=nws&sa=X&ved=2ahUKEwie8KTKsYj-AhWkU2wGHatNBAkQ_AUoAnoECAEQBA&biw=1536&bih=754&dpr=1.25"
#   headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
#   }
#   response = requests.get(search_url, headers=headers)
#   soup = BeautifulSoup(response.content, "lxml")

#   article_links = [tag.get("href")[30:] for tag in soup.find_all("a") 
#                    if tag.get("href") and tag.get("href").startswith('/url?esrc=s&q=&rct=j&sa=U&url=')]

#   article_data = []
#   article_title = []  # Initialize the list outside the loop

#   for link in article_links:
#     response_ = requests.get(link, headers=headers)
#     soup_ = BeautifulSoup(response_.content, "lxml")
#     title = soup_.find("title")
#     article_title.append(title.text if title else "Title Not Found")  
#     meta_tag = soup_.find('meta', attrs={'name': 'description'})
#     article_data.append(meta_tag.get('content') if meta_tag else "Description Not Found")

#   # ... (Rest of your code: Sentiment Analysis and Streamlit display)

#   # Load the sentiment analysis model
#   finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
#   tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
#   nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

#   # Perform sentiment analysis
#   article_info = [] 
#   for description, url, title in zip(article_data, article_links, article_title):
#     results = nlp(description)
#     article_info.append({"URL": url, 
#                          "Sentiment": results[0], 
#                          "Title": title}) 


#   return article_info

# # Streamlit App
# st.title("Bank News Sentiment Analyzer")
# bank_name = st.text_input("Enter a Stock Name:", "HDFC")

# if st.button("Analyze Sentiment"):
#     with st.spinner("Analyzing news articles..."):
#         results = getSentiment(bank_name)

#     st.subheader("Results:")
#     for article in results:
#         st.write(f"**Title:** {article['Title']}")
#         st.write(f"**URL:** {article['URL']}")
#         st.write(f"**Sentiment:** {article['Sentiment']['label']}, Score: {article['Sentiment']['score']:.3f}")
#         st.write("----") 
