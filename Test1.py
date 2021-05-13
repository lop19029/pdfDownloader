import os
import urllib3
from bs4 import BeautifulSoup as bs
import requests

"""
Returns the website tree
"""
def get_soup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = bs(response.data, features="html.parser")
    return soup

"""
Looks for a file in a soup. Returns the file link
"""
def get_download_link(path_end, url) :
    soup = get_soup(url)
    current_link = ''
    download_link = ''

    for link in soup.find_all('a'):
        current_link = link.get('href')
        if isinstance(current_link, str):
            if current_link.endswith(path_end):
                download_link = current_link
    return download_link
 
def main():    
    #Request the data using the document link
    download_link = get_download_link("Padrão_TISS_Componente_Organizacional_202103.pdf", "http://www.ans.gov.br/prestadores/tiss-troca-de-informacao-de-saude-suplementar/padrao-tiss-marco-2021")
    domain = "http://www.ans.gov.br"
    downloadURL = domain + download_link
    req = requests.get(downloadURL, stream = True)

    #create a new file in the directory where the program resides
    with open(os.path.join(os.path.abspath(__file__),'..',"Padrão_TISS_Componente_Organizacional_202103.pdf"), "wb") as pdf:
        #write the new file one chunk at a time
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)

if __name__ == "__main__":
    main()   

