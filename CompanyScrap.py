import requests
from bs4 import BeautifulSoup
import pandas as pd


def Get_Details(job_link):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    html = job_link
    try:
        r=requests.get(html, headers)
        search=BeautifulSoup(r.content,'html.parser')
        return(search)
    except:
        return(False)


def Extract_Details(company):

    try:
        scores = company.find_all('div', class_= 'css-zlzlxd eu4oa1w0')
        try:
            happiness_score = scores[0].text.strip()
        except:
            happiness_score = 'Na'
        try:
            appreciation_score = scores[1].text.strip()
        except:
            appreciation_score ='Na'
        try:    
            achievement_score = scores[2].text.strip()
        except:
            achievement_score = 'Na'
    except:
        happiness_score = 'Na'
        appreciation_score = 'Na'
        achievement_score = 'Na'
    try:    
        position_companyhead = company.find('span', class_='css-3j50sk e1wnkr790').text.strip()
    except:
        position_companyhead ='Na'
    try:
        companyhead = company.find('span', class_='css-1w0iwyp e1wnkr790').text.strip() 
    except:
        companyhead = 'Na'
    try:
        performancehead = company.find('span', class_='css-4oitjw e1wnkr790').text.strip()
    except:
        performancehead = 'Na'
    try:
        companyfounded = company.find('div', class_='css-1w0iwyp e1wnkr790').text.strip()
    except:
        companyfounded = 'Na'
    try:
        companysize = company.find('div', class_='css-1k40ovh e1wnkr790').text.strip()
    except:
        companysize = 'Na'
        
    Details = [happiness_score,appreciation_score,achievement_score,position_companyhead,companyhead,performancehead,companyfounded,companysize]
    return(Details)

company = Get_Details('')
if company:
    list_details = Extract_Details(company)
    print(list_details)
else:
    list_details=['Website not present' for x in range(8)]
    print(list_details)