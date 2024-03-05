FROM python:3.10.8

SHELL ["/bin/bash", "-c"]


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim redis-server

RUN useradd -rms /bin/bash topblog && chmod 777 /opt /run

WORKDIR /topblog

RUN mkdir /topblog/static && mkdir /topblog/media && chown -R topblog:topblog /topblog && chmod 755 /topblog

COPY --chown=topblog:topblog . .

RUN pip install -r requirements.txt
RUN pip install -U 'Twisted[tls,http2]'

USER topblog

CMD ["gunicorn","-b","0.0.0.0:8000","topblog.wsgi:application"]
