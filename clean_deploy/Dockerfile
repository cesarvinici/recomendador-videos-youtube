FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++ \
        gconf-service libasound2 libatk1.0-0 \ 
        libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
        libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 \
        libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 \
        libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 \
        libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 \
        libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 \
        lsb-release xdg-utils wget
        
RUN pip install -r requirements.txt
# RUN python db_starter.py
#CMD python ./app.py

ENTRYPOINT [ "streamlit", "run" ]

# Run the image as a non-root user
#RUN adduser -D myuser
#USER myuser
# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 
#CMD gunicorn --bind 0.0.0.0:80 wsgi 
# CMD streamlit run app.py --server.port $PORT

#https://github.com/microsoft/LightGBM/blob/master/docker/dockerfile-python
#https://github.com/heroku/alpinehelloworld
#https://devcenter.heroku.com/articles/container-registry-and-runtime

#⬢ murmuring-peak-72081
#https://murmuring-peak-72081.herokuapp.com/ | https://git.heroku.com/murmuring-peak-72081.git
