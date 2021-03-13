FROM python:3.9.2-slim


RUN mkdir -p /tmp/ssq/Spider

# copy application
COPY Py/Spider /tmp/ssq/Spider
COPY Py/setup.py /tmp/ssq/

# Install application
RUN pip install pip --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    cd /tmp/ssq && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python /tmp/ssq/setup.py install && \
    rm -rf /tmp/ssq

# Add user
RUN useradd --create-home --shell /bin/bash ssq

VOLUME /data
COPY DB/SQLite/ssq.db /data/

USER ssq

WORKDIR /home/ssq

ENTRYPOINT ["ssq"]

CMD ["--db-file", "/data/ssq.db", "download", "--query-count", "30"]
