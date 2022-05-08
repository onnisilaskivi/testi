#Dockerfile, Image, Container
FROM python:3.8

ADD main.py .
ADD beer2.png .
ADD mato.png .

RUN pip install tkinter PIL random

CMD ["python", "/.main.py"]
