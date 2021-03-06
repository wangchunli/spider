from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json

def getCountry(ipAddress):
	try:
		response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
	except HTTPError as e:
		return None
	responseJson = json.loads(response)
	return responseJson.get("country_code")
def getLinks(articleUrl):
	html=urlopen("http://en.wikipedia.org"+articleUrl)
	bsObj=BeautifulSoup(html,'html.parser')
	return bsObj.find("div",{"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Python_(programming_language)")

def getHistoryIPs(pageUrl):
	pageUrl = pageUrl.replace("/wiki/","")
	historyUrl="http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
	print("historyUrl "+historyUrl)
	html=urlopen(historyUrl)
	bsObj = BeautifulSoup(html,'html.parser')
	ipAddresses = bsObj.findAll("a",{"class":"mw-anonuserlink"})
	addressList = set()
	for ipAddress in ipAddresses:
		addressList.add(ipAddress.get_text())
	return addressList

for link in links:
	print("------------------")
	historyIps=getHistoryIPs(link.attrs["href"])
	for historyIP in historyIps:
		country=getCountry(historyIP)
		if country is not None:
			print(historyIP+" is from "+country)
