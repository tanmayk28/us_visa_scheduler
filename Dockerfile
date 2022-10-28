FROM python:alpine

RUN apk add git
RUN git clone https://github.com/tanmayk28/us_visa_scheduler.git /app

WORKDIR "/app"
RUN pip install -r requirements.txt
RUN chmod 755 visa.py

COPY config.ini config.ini

ENTRYPOINT ["./visa.py"]
