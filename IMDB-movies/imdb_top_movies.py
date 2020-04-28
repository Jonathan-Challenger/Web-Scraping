# Importing beatifulsoup
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup

# Base url with all urls of interest in 
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

# Reading base URL
uClient = ureq(url)
page_html = uClient.read()
uClient.close()

# Using beatifulsoup to parse page
page_soup = soup(page_html, "html.parser")

# Finding the area of page that contains link
link_container = page_soup("td", {"class":"titleColumn"})

# Creating empty list and filling it with links of interest
links = []
for i in link_container:
	link = i.find("a", href = True)
	mov = ("https://www.imdb.com" + link['href'])
	links.append(mov)
		

# Creating file to put information in
filename = "movie_info.csv"
f = open(filename, "w")

# Creating headers for file and adding them to file
headers = "Title, Rating, Rating_Count, Genre\n"
f.write(headers)

# Iterate through movie links list and extracting title, rating, rating count and genre for every movie and writing it to file
for i in links:
	uClient = ureq(i)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	title = page_soup.findAll("h1")
	movie_title = title[0].text.strip()

	rating = page_soup.findAll("span", {"itemprop":"ratingValue"})
	rating_star = rating[0].text

	ratings = page_soup.findAll("span", {"itemprop":"ratingCount"})
	rating_count = ratings[0].text

	genre1 = page_soup.findAll("div", {"class":"subtext"})
	genre = genre1[0].find("a").text

	
	f.write(movie_title.replace(",", "") + "," + rating_star + "," + rating_count.replace(",", "") + "," + genre + "\n")


# Closing file
f.close()