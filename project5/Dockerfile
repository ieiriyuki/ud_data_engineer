FROM python:3.7.7

ARG AIRFLOW_VERSION="1.10.10"
ARG AIRFLOW_EXTRAS="async,aws,azure,celery,crypto,dask,elasticsearch,gcp,kubernetes,mysql,postgres,redis,slack,ssh,statsd,virtualenv"
ARG AIRFLOW_HOME="/opt/airflow"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    netcat \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip setuptools wheel \
    && pip install \
    docutils==0.15 \
    websocket_client==0.54.0 \
    apache-airflow[${AIRFLOW_EXTRAS}]==${AIRFLOW_VERSION}

WORKDIR ${AIRFLOW_HOME}

COPY . .

EXPOSE 8080

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]

CMD [ "bash" ]
