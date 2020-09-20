import streamlit as st
from settings import SRC_DIR, DATA_DIR, ROOT_DIR
import json
import os
import re
from DAO.database import Database

def main():
    st.header("Recomendador de vídeos do Youtube")

    st.subheader("Sobre o projeto")
    st.write('Recomendador de videos criado no curso "Como Criar uma Solução Completa de Data Science" do Mario Filho.')
    st.write('''Nas aulas foi demonstrado métodos de busca de dados do Youtube bem como alguns modelos de classificação
    e o deploy de uma aplicação utilizando o framework flask lendo de uma pequena base de registros em json.''')

    st.write('''Para o presente projeto o FrontEnd foi migrado para o Streamlit devido a facilidade de utilizar
    alguns elementos visuais, também foi removido o o arquivo json e todo o acesso é feito via banco de dados SqLite3.''')

    st.subheader("Coleta de dados e recomendação de novos vídeos")
    st.write('''Considerando que o recomendador trata apenas de vídeos de Machine Learning e Data Science foi agendado alguns cron jobs
    para buscar, salvar e fazer a recomendação de novos vídeos uma vez por semana.''')
    st.write('''Uma vez por mês o modelo será treinado novamente com vídeos os videos antigos e novos de forma a melhorar cada vez mais o score
    com base em vídeos que eu forem marcados como Gostei ou Não Gostei.''')


    st.header("Ultimas recomendações: ")
    videos = []
    database = Database()
    videos = database.show_videos()
    for video in videos:  
        id, title, video_link, thumbnail, score, liked = video
        score = round(score * 100, 2)
        st.markdown("[{title}](https://youtube.com/{url})".format(title=title, url=video_link))
        st.write(
        f'<iframe width="680" height="400" src="https://youtube.com/embed/{video_id(video_link)}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        unsafe_allow_html=True,
    )
       
        st.text(f"Score: {score}%")

        options = ('Não gostei','Gostei')
        gostei = st.radio('Marcar vídeo:', options , liked, key=id)
        
        if gostei == 'Gostei':
            set_liked_video(1, id)
        else:
            set_liked_video(0, id)

        st.markdown("---")

def set_liked_video(value, id):
    ''' calls method that will set video as liked or not '''
    database = Database()
    database.like_video(value, id)


def video_id(video_link):
    ''' extracts video id from link '''
    return re.split(r'v=(\w*)', video_link)[1]


if __name__ == "__main__":
    main()