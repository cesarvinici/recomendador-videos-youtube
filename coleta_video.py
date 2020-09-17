import os
import pandas as pd
import json
import time
import re
import glob
from bs4 import BeautifulSoup as bs 
from requests_html import HTMLSession
from tqdm import tqdm

class ColetaDeDadosVideo(): 

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    HTML_DIR = os.path.join(CURRENT_DIR, "dados_brutos/")
    URL = "https://www.youtube.com{link}"

    def __init__(self, lista_de_links):
        self.lista_de_links = lista_de_links
        self.processa_videos()
        self.coleta_de_dados()

    def processa_videos(self):
        try:
            for link in self.lista_de_links:
                session = HTMLSession()
                uri = self.URL.format(link=link)
                print(uri)
                link_name = re.search("v=(.*)", link).group(1)
                response = session.get(uri)
                # executando Java-script
                response.html.render()

                with open(os.path.join(self.HTML_DIR, f"video_{link_name}.html"), 'w+', encoding='utf8') as output:
                    output.write(response.html.html)
                time.sleep(5)
        except BaseException:
            print(f"Problema ao salvar os dados do video - {link_name}")

    def coleta_de_dados(self):
        with open("parsed_video_info.json", "w+") as output:
            for video_file in tqdm(sorted(glob.glob(self.HTML_DIR+"/video*"))):
                with open(video_file, "r+") as inp:
                    page_html = inp.read()
                    parsed = bs(page_html, 'html.parser')

                    class_watch = parsed.find_all(attrs={"class": re.compile(r"watch")})
                    id_watch = parsed.find_all(attrs={"id": re.compile(r"watch")})
                    channel = parsed.find_all("a", attrs={"href": re.compile(r"channel")})
                    meta = parsed.find_all("meta")

                    data = dict()

                    for e in class_watch:
                        colname = "_".join(e['class'])
                        if "clearfix" in colname or re.match(r"^css-https.*", colname):
                            continue
                        data[colname] = e.text.strip()
                    
                    for e in id_watch:
                        colname = e['id']
                        # if "clearfix" in colname:
                        #     continue
                        # print(colname)
                        data[colname] = e.text.strip()

                    for e in meta:
                        colname = e.get("property")
                        if colname is not None:
                            data[colname] = e['content']

                    for link_num, e in enumerate(channel):
                        data[f"channel_link_{link_num}"] = e['href']


                    output.write(f"{json.dumps(data)}\n")
if __name__ == "__main__":
    df = pd.read_json("parsed_videos.json", lines=True)
    lista_de_links = df['link'].unique()
    ColetaDeDadosVideo(lista_de_links)