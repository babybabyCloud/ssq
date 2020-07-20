FROM python:3.8-slim

# Install firefox
RUN apt-get update && \
    apt-get install -y firefox-esr && \
    apt-get clean && \
    apt-get autoremove && \ 
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/ssq/Spider

# copy application
COPY Py/Spider /tmp/ssq/Spider
COPY Py/setup.py /tmp/ssq/

# Install application
RUN pip install pip --upgrade && \
    cd /tmp/ssq && \
    python /tmp/ssq/setup.py install && \
    rm -rf /tmp/ssq

# Add user
RUN useradd --create-home --shell /bin/bash ssq

VOLUME /data
COPY DB/SQLite/ssq.db /data/

USER ssq

WORKDIR /home/ssq

ENTRYPOINT ["ssq"]

CMD ["download", "--db-file", "/data/ssq.db", "--query-count", "30"]
