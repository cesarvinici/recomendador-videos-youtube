import os
import pandas as pd
import json
import time
from bs4 import BeautifulSoup as bs 
from requests_html import HTMLSession
from tqdm import tqdm


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(CURRENT_DIR, "dados_brutos/")
TOTAL_DE_PAGINAS_PARA_SALVAR = 3
QUERIES = ['machine+learning', 'data+science', "kaggle"]
URL = "https://www.youtube.com/results?search_query={query}&sp=EgIIAg%253D%253D&p={page}"


def buscar_paginas():
    for query in tqdm(QUERIES, "Buscando páginas no youtube"):
        for page in range(1, TOTAL_DE_PAGINAS_PARA_SALVAR+1):
            session = HTMLSession()
            # inserindo a query e o numero da pagina na url
            uri = URL.format(query=query, page=page)
            print(uri)
            # enviado requisição para o youtube
            response = session.get(uri)
            # executando Java-script
            response.html.render(sleep=1)
            # Salvando arquivo HTML na pasta dados_brutos
            with open("./dados_brutos/{}_{}.html".format(query, page), 'w+', encoding='utf8') as output:
                output.write(response.html.html)
            time.sleep(2)


def processando_dados():
    for query in  tqdm(QUERIES, "Processando os dados brutos"):
        for page in range(1,TOTAL_DE_PAGINAS_PARA_SALVAR+1):
            # Lendo arquivos html
            with open("./dados_brutos/{query}_{page}.html".format(query=query, page=page), 'r+') as inp:
                page_html = inp.read()
                # Processando a página html
                parsed = bs(page_html, "html.parser")
                # Buscando todas as tags "a" com o id "video-title"
                ancors = parsed.find_all('a', attrs={"id": "video-title"})
                for e in ancors:
                    link = e['href']
                    title = e['title']
                    # Salvando os dados
                    with open("parsed_videos.json", "a+", encoding='utf8') as output:
                        data = {"link": link, "title": title, "query": query}
                        output.write("{}\n".format(json.dumps(data)))



if __name__ == "__main__":
    buscar_paginas()
    processando_dados()