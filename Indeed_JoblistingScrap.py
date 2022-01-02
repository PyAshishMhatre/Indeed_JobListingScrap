# Import Libs --- Requests, BeautifulSoup4 and Pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Enter key word for job title search
Search_title = ('%20'.join(input('Enter Job Title').split())).strip()

#Get function requests webpage and parse the html
def Get(page, Search_title = 'data%20analyst'):
    #specify user agent to avoid getting ban on website
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    #Stitch together to form URL
    html = f'https://www.indeed.com/jobs?q={Search_title}&l=United%20States&explvl=entry_level&start={page}'
    #Access URL using Requests
    r=requests.get(html, headers)
    #Parse the HTML
    search=BeautifulSoup(r.content,'html.parser')
    return(search)
    
def Extract(soup):
    #Extracting Data from HTML
    jobs = soup.find_all('div', class_ ="job_seen_beacon")
    #Looping through required information blocks
    for job in jobs:
        job_title = job.find('h2').text.strip()
        company_name =  job.find('span', class_ = 'companyName').text.strip()
        try:
            company_link = (job.find('span', class_ = 'companyName').find('a', class_="turnstileLink companyOverviewLink"))["href"].strip()
            company_link = 'https://www.indeed.com' + company_link
        except:
            company_link = ''
        company_loc = job.find('div', class_='companyLocation').text.strip()
        try:
            summary = job.find('li').text
        except:
            summary = ''
        try:
            job_comp = job.find('div', class_='attribute_snippet').text.strip()
        except:
            job_comp = ''
        
        #Call on individual company websites to get extra details 
        company = Get_Details(company_link)
        #Validate the company URL
        if company:
            list_details = Extract_Details(company)
            #print(list_details)
        else:
            #Return 'Website not present' for missing company pages
            list_details=['Website not present' for x in range(8)]
            #print(list_details)
        
        #Combine all data in Dict
        Company_Dict = {
            'Job_Title' : job_title,
            'Company_Name' : company_name,
            'Company_Link' : company_link,
            'Company_location' : company_loc,
            'Company_summary' : summary,
            'Salary' : job_comp,
            'Happiness_Score': list_details[0], #Extract company details from returned list
            'Appreciation_Score': list_details[1],
            'Achievement_Score': list_details[2],
            'CompanyHead_Position': list_details[3],
            'Company_Head': list_details[4],
            'Performance_Rating': list_details[5],
            'CompanyFoundedYear': list_details[6],
            'Company_Size': list_details[7],
            }
        #Append respective company data to form list of companies data
        data.append(Company_Dict)
    return(data)

#Request company pages and Parse HTML
def Get_Details(job_link):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    html = job_link
    #Validate Company website, upon successful validation extract data.
    try:
        r=requests.get(html, headers)
        search=BeautifulSoup(r.content,'html.parser')
        return(search)
    #Return False on unsuccessful validation
    except:
        return(False)

#Extract details from company webpage
def Extract_Details(company):
    #Exception handling for irregular information data on each company webpage
    #Extract all present data, Replace with 'NA' for any missing information
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
    #Store and return all data into a list format    
    Details = [happiness_score,appreciation_score,achievement_score,position_companyhead,companyhead,performancehead,companyfounded,companysize]
    return(Details)

#Initialize main list structure for storing all data
data = []
#Loop through multiple pages to Extract all pages for Job posting
for i in range(0,70,10):
    soup = Get(i, Search_title)
    Extract(soup)
#Convert to DataFrame
Joblisting = pd.DataFrame(data)
#Name the file according to format 'JobTitle_Date'
file_name = input('Enter File name')
#Write Dataframe to CSV.
Joblisting.to_csv(f'{file_name}.csv')