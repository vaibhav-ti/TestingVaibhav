FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
ADD . /usr/src/app/
RUN pip3 install -r requirements.txt

RUN apt-get update && apt install python3-pip --yes --force-yes && pip install gunicorn

EXPOSE 8000
CMD ["/bin/bash", "scripts/entrypoint.sh"]