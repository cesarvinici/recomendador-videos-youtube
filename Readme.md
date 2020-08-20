# Recomendador de videos do Youtube (WORK IN PROGRESS)

#### Qual o problema?
     Gastar muito tempo buscando novos vídeos no youtube.
     
#### Qual  a solução ideal?
     Ter uma lista apenas dos vídeos que eu vou gostar.

#### Como posso fazer isso com Data Science/Machine Learning?
     Criando uma solução de recomendador que busca os vídeos todos os dias no youtube e envia para mim.
     
#### Como essa solução será usada em produção?
     web app com os vídeos (link) e as previsões ordenadas
* Abordagens
  - Ponto de corte -> retorna os top 'n'
  - Ranking -> Ordena os vídeos mais interessantes primeiro

#### Como eu vou saber que deu certo?
     Métrica primária: Dos top n vídeos quantos eu coloco na lista de watch later.
     Os top n recomendados são mais assistidos que os top N da busca do youtube.
     Métrica secundária: Quanto tempo eu passo selecionando vídeos.