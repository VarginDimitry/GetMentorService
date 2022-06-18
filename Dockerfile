FROM python:3.9.4-buster

WORKDIR /GetMentorService
ENV PYTHONPATH="/GetMentorService"
ADD . /GetMentorService/
RUN pip install -r ./requirements.txt

EXPOSE 5000

#CMD [ "python", "/GetMentorService/main.py", "--config", "DockerConfig" ]
CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi:app"]