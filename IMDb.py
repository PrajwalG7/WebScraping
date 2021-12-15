# Scraping IMDb

import requests
from bs4 import BeautifulSoup
import html5lib
import csv
import pandas as pd

r=requests.get("https://www.imdb.com/search/title/?groups=top_1000")
print(r)

soup=BeautifulSoup(r.text,"html.parser")
# Initialize the lists to store data
titles=[]
years=[]
time=[]
imdb_rating=[]
genre=[]
votes=[]

movie_div=soup.find_all("div", class_="lister-item mode-advanced")
# get into class to extract all the content
for movieSection in movie_div:
    name=movieSection.h3.a.text
    titles.append(name)
    year=movieSection.h3.find("span", class_="lister-item-year").text
    years.append(year)
    ratings = movieSection.strong.text
    imdb_rating.append(ratings)
    category = movieSection.find("span", class_="genre").text.strip()
    genre.append(category)
    runTime = movieSection.find("span", class_="runtime").text
    time.append(runTime)
    """
    As from the image, we can see that we have two span tags with classname="nv". 
    So, for votings we need to consider nv[0] and for gross collections nv[1]
    """
    nv = movieSection.find_all("span", attrs={"name": "nv"})
    vote = nv[0].text
    votes.append(vote)

"""
Now we will build a DataFrame with pandas To store the data we have to create nicely into a table,
so that we can really understand And we can do it.
"""
movies = pd.DataFrame(
    {
        "Movie": titles,
        "Year": years,
        "RunTime": time,
        "imdb": imdb_rating,
        "Genre": genre,
        "votes": votes
    }
)
print(movies)

# cleaning the data
movies["Year"] = movies["Year"].str.extract("(\\d+)").astype(int) #Extracting only numerical values. so we can commit "I"
movies["RunTime"] = movies["RunTime"].str.replace("min", "minutes") #replacing <b>min</b> with <b>minutes</b>
movies["votes"] = movies["votes"].str.replace(",", "").astype(int) #removing "," to make it more clear

print(movies)


# storing the data to .csv (create afile with .csv extension.)
movies.to_csv(r"C:\Users\Aryan\PycharmProjects\pythonProject\FirstDirect\PythonProjects\WebScraping\movies.csv",index=False, header=True)
