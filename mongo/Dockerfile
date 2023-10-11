FROM mongo:4.4

RUN apt update && apt install -y unzip

COPY ./init /docker-entrypoint-initdb.d
RUN chmod -R 777 /docker-entrypoint-initdb.d

COPY rarbg /rarbg

RUN cat /rarbg/x* > /rarbg/rarbg.zip
RUN unzip /rarbg/rarbg.zip -d /rarbg
RUN rm /rarbg/rarbg.zip /rarbg/x*   

EXPOSE 27017
