FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY static static
COPY templates templates
COPY app.py boot.sh config.py models.py tests.py ./
RUN chmod a+x boot.sh

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]