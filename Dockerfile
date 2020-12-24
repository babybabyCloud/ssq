FROM python:3.8-slim AS firefox

ARG firefoxVersion=84.0.1
ARG firefoxTarFile=firefox-${firefoxVersion}.tar.bz2

RUN apt-get update && \
    apt-get install -y wget tar bzip2

# Install firefox
RUN wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/84.0.1/linux-x86_64/en-US/${firefoxTarFile} > /dev/null && \
    tar -xjf ${firefoxTarFile} -C /usr/lib/

FROM python:3.8-slim
COPY --from=firefox /usr/lib/firefox /usr/lib/firefox 

RUN mkdir -p /tmp/ssq/Spider

# copy application
COPY Py/Spider /tmp/ssq/Spider
COPY Py/setup.py /tmp/ssq/

# Install application
RUN pip install --upgrade pip && \
    cd /tmp/ssq && \
    python setup.py install && \
    rm -rf /tmp/ssq

# Add user
RUN useradd --create-home --shell /bin/bash ssq

VOLUME /data
COPY DB/SQLite/ssq.db /data/

USER ssq

WORKDIR /home/ssq

ENTRYPOINT ["ssq"]

CMD ["--db-file", "/data/ssq.db", "download", "--query-count", "30"]
