FROM python:2.7

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY flask/ .

CMD ["python", "./runserver.py"]

EXPOSE 5000
