# aqui vao os codigos do scrapper da luiza
import requests
from bs4 import BeautifulSoup
def wbscrp(input):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    if input != None:
        p = input.replace(' ', '-')
        p = p.lower()

        url = 'https://www.sunoresearch.com.br/noticias/tags/{}'.format(p)

        with requests.Session() as s:
            noticias = s.get(url, headers=headers)
            soup = BeautifulSoup(noticias.text, 'lxml')
            pol = soup.text
            soup2 = soup.find_all('div', class_="cardsPage__listCard__boxs__content")
            
            pop = len(soup2)
            # soupb=soup2[0]
            # llink=soupb.a['href']
            # ttit=soupb.a.h2.text
            # notic = s.get(llink, headers=headers)
            # notic_content = BeautifulSoup(notic.text, 'lxml')
            # soupn=notic_content.find_all('p')
            # sopi=soupn[0]
            # for sopi in soupn:
            #   sopil=sopi.text
            #  print(sopil)
            # sopi=(soupn[0]).text
            aa=[]
            for soupb in soup2:
                llink = soupb.a['href']
                ttit = soupb.a.h2.text
                #print(llink)
                #print(ttit)
                notic = s.get(llink, headers=headers)
                #print(notic)
                notic_content = BeautifulSoup(notic.text, 'lxml')
                soupn = notic_content.find_all('p')
                for sopi in soupn:
                    sopil = sopi.text
                    aa.append(sopil)

    else:
        llink=''
        ttit=''
        aa=[]

    return aa
