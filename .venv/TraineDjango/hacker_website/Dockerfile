FROM python:3.9-slim as production

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

COPY requarenment.txt ./requarenment.txt
RUN pip install -r ./requarenment.txt

COPY manage.py ./manage.py
COPY setup.cfg ./setup.cfg
COPY hacker_website ./hacker_website

EXPOSE 8000
