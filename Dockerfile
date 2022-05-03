FROM python:3.9.4-buster

WORKDIR /GetMentorService
ENV PYTHONPATH="/GetMentorService"

COPY ./ ./
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 5000 5000

CMD [ "python", "/GetMentorService/main.py" ]