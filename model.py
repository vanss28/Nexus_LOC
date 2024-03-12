from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro")
text = '''The broader trend of Nity 50 is positive and some contribution has been given by Reliance Industries (NS:RELI) Limited which holds a weightage of 10.44%, making it the second-highest weighted stock in the index. The company has a market capitalization of INR 20,33,765 crore and is engaged in refining, and manufacturing of refined petroleum products, and petrochemicals, including manufacturing of basic chemicals, fertilizers and nitrogen compounds, plastic and synthetic rubber in primary forms.
The stock has rallied over 20% in the last 3 months, which is commendable for such a gigantic stock. However, as the stock delivered gains, it also became overvalued and now the market seems to be realizing that. The stock is now slowing down on its way up as profit booking is kicking in."  # Replace with actual articles
'''
response = model.generate_content(["""Determine which stock(ticker) market sectors are likely to be affected by the news.
  Output:
  Sector:
""", text]) 

candidates = response.candidates 

# Access the first candidate 
candidate = candidates[0] 
content = candidate.content 

# Access the different text parts and join them
text = content.parts

print(content.parts)
