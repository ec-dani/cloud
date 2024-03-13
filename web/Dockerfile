FROM python:3.9
COPY app.py /web/app.py
COPY templates /web/templates
COPY static /web/static
RUN pip install flask pymongo pyopenssl
RUN openssl req -x509 -newkey rsa:4096 -nodes -out myCert.pem -keyout myKey.pem -subj "/C=SE/ST=./L=Eskilstuna/O=DVA260/OU=/CN=" -days 365
CMD ["python3","/web/app.py"]