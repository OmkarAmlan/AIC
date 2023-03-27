from google_play_scraper import Sort, reviews
import collections
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()

result, continuation_token = reviews(
    'com.baazigames.pokerbaazi.free',
    lang='en', 
    country='us', 
    sort=Sort.NEWEST,
)

result, _ = reviews(
    'com.baazigames.pokerbaazi.free',
)
i=len(result)
k=0
count=0
L=[]

#Find occuring words among negative reviews.
para=""
word_index={}
while k<i:
    if(result[k]['score']<=2):
        line_text=result[k]['content'].lower().replace('!',"").replace(',',"").replace('.',"").replace('?',"").replace('$',"").replace('%',"").replace("/","")
        para+=line_text
        count+=1
    k+=1
word_index=collections.Counter(para.split()).most_common()
print("Index of occuring negative words in reviews with score of <= 2:")
check=["fraud","scam","lost","blocked","issues","bad","verification","slow","care","blocking","cheated","cheat","cheating","ad","ads","issue","bugged","bugs","bug","fake","bots","cheated","suicide","trust","crashing","failed","looted","cheat","waste"]
length=len(word_index)
b=0
while b<length:
    if word_index[b][0] in check:
        print(word_index[b][0],word_index[b][1],sep=" ")
    b+=1
    
print("\n")
print("Count of reviews with score <= 2 is " + str(count) + "\n")

#Run sentimental analysis on an unbiased set of 100 reviews from play store.
L=[]
sentimentOutput=[]
j=0
countbase=0
while j<i:
    line_text2=result[j]['content'].lower().replace('!',"").replace(',',"").replace('.',"").replace('?',"").replace('$',"").replace('%',"").replace("/","")
    L.append(line_text2)
    countbase+=1
    j+=1
print("Total unbiased review base = "+str(j))
for row in L:
    sentimentOutput.append(sentiment.polarity_scores(row))

sumpos=0
sumneg=0
pos=0
neg=0
neu=0
sumneu=0
sumcomp=0

for i in range(len(sentimentOutput)):
    if(sentimentOutput[i]['compound']==0):
        neu+=1
    elif(sentimentOutput[i]['compound']>0):
        pos+=1
    else:
        neg+=1
    sumpos+=sentimentOutput[i]['pos']
    sumneg+=sentimentOutput[i]['neg']
    sumneu+=sentimentOutput[i]['neu']
    sumcomp+=sentimentOutput[i]['compound']

avgpos=sumpos/len(sentimentOutput)
avgneg=sumneg/len(sentimentOutput)
avgnue=sumneu/len(sentimentOutput)
avgcomp=sumcomp/len(sentimentOutput)

#Represents the average positive review while considering every single parameter on every review. 
#To compare the compound average with the average positive and negative review while considering each individual review.
print("Average positive review = " + str(avgpos))
print("Average negative review = " + str(avgneg))
print("Average neutral review = " + str(avgnue))
print("Compound average = " + str(avgcomp))
print("\n")

#Find the percentage of positive, negative and neutral reviews based off of the individual compound rating.
print("Positive Reviews = " + str(pos*100/len(sentimentOutput)) + " %")
print("Negative Reviews = " + str(neg*100/len(sentimentOutput)) + " %")
print("Neutral Reviews = " + str(neu*100/len(sentimentOutput)) + " %")
print("\n")

#Web data from Web-scraping.
excel_data_df = pd.read_excel("C:/Users/crash/Desktop/College Work/Revendous Case Study/Run_ResultsEx.xlsx")
WebL=(excel_data_df['Content'].tolist())

#sentimental analysis on unbiased set of reviews.
print("Web data Sentimental analysis")
WebDataSA=[]
for temp in WebL:
    WebDataSA.append(sentiment.polarity_scores(row))

sumpos1=0
sumneg1=0
pos1=0
neg1=0
neu1=0
sumneu1=0
sumcomp1=0

for o in range(len(WebDataSA)):
    if(sentimentOutput[o]['compound']==0):
        neu1+=1
    elif(sentimentOutput[o]['compound']>0):
        pos1+=1
    else:
        neg1+=1
    sumpos1+=sentimentOutput[o]['pos']
    sumneg1+=sentimentOutput[o]['neg']
    sumneu1+=sentimentOutput[o]['neu']
    sumcomp1+=sentimentOutput[o]['compound']

avgpos1=sumpos/len(WebDataSA)
avgneg1=sumneg/len(WebDataSA)
avgnue1=sumneu/len(WebDataSA)
avgcomp1=sumcomp/len(WebDataSA)

#Represents the average positive review while considering every single parameter on every review. 
#To compare the compound average with the average positive and negative review while considering each individual review.
print("Average positive review = " + str(avgpos1))
print("Average negative review = " + str(avgneg1))
print("Average neutral review = " + str(avgnue1))
print("Compound average = " + str(avgcomp1))
print("\n")

#Find the percentage of positive, negative and neutral reviews based off of the individual compound rating.
print("Positive Reviews = " + str(pos1*100/len(WebDataSA)) + " %")
print("Negative Reviews = " + str(neg1*100/len(WebDataSA)) + " %")
print("Neutral Reviews = " + str(neu1*100/len(WebDataSA)) + " %")
print("\n")
