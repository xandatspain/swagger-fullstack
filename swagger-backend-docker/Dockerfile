FROM python:3.5.1-alpine

COPY requirements.txt /requirements.txt
COPY swagger-backend.py /swagger-backend.py

RUN pip install -r /requirements.txt && chmod 755 /swagger-backend.py

CMD ["/swagger-backend.py"]





