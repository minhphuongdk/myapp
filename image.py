from bs4 import BeautifulSoup
import requests
def find_image(name):
	url1='https://www.google.com.vn/search?q='
	keyword=name
	fil=len(keyword.split(' '))
	startfil=fil+7
	url2='&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiGq6WplNrdAhXFfSsKHa9EAjMQ_AUICigB&biw=1920&bih=948'
	url=url1+keyword+url2
	r=requests.get(url)
	c=r.content
	soup=BeautifulSoup(c,"html.parser")
	soup=soup.findAll('img')
	soup=str(soup[1])
	soup=soup.replace('<img','').replace('/>','').split(' ')
	soup=soup[startfil].replace('src="','').replace('"','')
	return (soup)
find_image('iphone 5')
