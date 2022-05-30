FROM python:3.9.4-buster

WORKDIR /GetMentorService
ENV PYTHONPATH="/GetMentorService"
#ENV GROUP_ID=1000 \
#    USER_ID=1000

#RUN addgroup -gid $GROUP_ID www
#RUN adduser -D -u $USER_ID -group www www -shell /bin/sh

#USER www

ADD . /GetMentorService/
RUN pip install -r ./requirements.txt

EXPOSE 5000

#CMD [ "python", "/GetMentorService/main.py", "--config", "DockerConfig" ]
CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi:app"]