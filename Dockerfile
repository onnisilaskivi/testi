#Dockerfile, Image, Container
FROM python:3.8

ADD main.py .
ADD beer2.png .
ADD mato.png .

RUN pip install tk Pillow random2

CMD ["python", "/.main.py"]
