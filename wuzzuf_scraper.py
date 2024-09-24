#edit
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import math

def wuzzuf_scrape(search_txt):
    search_keywords = search_txt.split()

    print(f"Scraping search results for : {search_txt}")

    base_url = f"https://wuzzuf.net/search/jobs/?q={'%20'.join(search_keywords)}&a=hpb"
    
    
    response = requests.get(base_url)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    results_per_page = 15
    
    num_of_results = int(soup.find('span', {'class':'css-xkh9ud'}).strong.text.replace(',',''))
    if(num_of_results == 0):
        print("No results found")
        return
    
    num_of_pages = math.ceil(num_of_results / results_per_page)

    titles_lst = []
    links_lst = []
    occupations_lst = []
    companies_lst = []
    specs_lst = []
    companies_locations_lst = []
    
    titles = soup.find_all("h2", {"class" : "css-m604qf"})
    titles_lst.extend([title.a.text for title in titles])
    links_lst.extend([title.a["href"] for title in titles])
    
    occupations = soup.find_all("div", {"class" : "css-1lh32fc"})
    occupations_lst.extend([list(occupation.stripped_strings) for occupation in occupations])
    
    companies = soup.find_all("a" , {"class" : "css-17s97q8"})
    companies_lst.extend([company.text.strip("-") for company in companies])

    companies_locations = soup.find_all("span", {"class" : "css-5wys0k"})
    companies_locations_lst.extend([company_location.text for company_location in companies_locations])
    
    specs = [spec.find('div', {'class':None}) for spec in soup.find_all('div', {'class':'css-y4udm8'})]
    specs_lst.extend([spec.text for spec in specs])
    
    for i in range(1,num_of_pages):
        response = requests.get(base_url+f"&start={i}")
        soup = BeautifulSoup(response.content, 'lxml')
    
        titles = soup.find_all("h2", {"class" : "css-m604qf"})
        titles_lst.extend([title.a.text for title in titles])
        links_lst.extend([title.a["href"] for title in titles])
    
        occupations = soup.find_all("div", {"class" : "css-1lh32fc"})
        occupations_lst.extend([list(occupation.stripped_strings) for occupation in occupations])
    
        companies = soup.find_all("a" , {"class" : "css-17s97q8"})
        companies_lst.extend([company.text.strip("-") for company in companies])


        companies_locations = soup.find_all("span", {"class" : "css-5wys0k"})
        companies_locations_lst.extend([company_location.text for company_location in companies_locations])
    
        specs = [spec.find('div', {'class':None}) for spec in soup.find_all('div', {'class':'css-y4udm8'})]
        specs_lst.extend([spec.text for spec in specs])

    assert len(specs_lst) == num_of_results
    assert len(companies_lst) == num_of_results
    assert len(occupations_lst) == num_of_results
    assert len(links_lst) == num_of_results
    assert len(titles_lst) == num_of_results
    assert len(companies_locations_lst) == num_of_results

    print(f"Search results for '{search_txt}' scraped successfully")
    

    dt = pd.DataFrame({'Title': titles_lst, 'Occupation' : occupations_lst, 'Company' : companies_lst, 'Company Location' : companies_locations_lst, 'Specs' : specs_lst, 'Link' : links_lst})

    dt.to_csv(f"{"_".join(search_keywords)}.csv")

    return dt

if __name__ == '__main__':
    wuzzuf_scrape(sys.argv[1].strip("'").strip('"'))
