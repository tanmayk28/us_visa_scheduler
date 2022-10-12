FROM python:alpine

RUN apk add git
RUN git clone https://github.com/yaoxiaoqi/mew_rescheduler.git /app

WORKDIR "/app"
RUN pip install -r requirements.txt
RUN chmod 755 visa.py

COPY config.ini config.ini

ENTRYPOINT ["./visa.py"]
