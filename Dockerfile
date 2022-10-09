FROM python:alpine

RUN apk add git
RUN git clone https://github.com/yaoxiaoqi/mew_rescheduler.git /app
RUN cd /app
RUN pip install -r requirements.txt
RUN chmod 755 visa.py

COPY config.ini /app/config.ini

ENTRYPOINT ["./visa.py"]
