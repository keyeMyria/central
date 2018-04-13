FROM python:3.6

ENV LIBRARY_PATH=/lib:/usr/lib
EXPOSE 8000
WORKDIR /app

COPY . /app
RUN pip install gunicorn && pip install -r /app/requirements.txt;chmod +x /app/run.sh

CMD /app/run.sh