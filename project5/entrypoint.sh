#!/usr/bin/bash

AIRFLOW__CORE__FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")

: ${AIRFLOW__WEBSERVER__WORKERS:=2}
: ${MYSQL_USER:=airflow}
: ${MYSQL_PASSWORD:=airflow}
: ${MYSQL_DATABASE:=airflow}
: ${MYSQL_PORT:=3306}
: ${MYSQL_HOST:=mysql}
: ${AIRFLOW__CORE__SQL_ALCHEMY_CONN:=mysql+mysqldb://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DATABASE}

PIP_VERSION=$(pip --version | cut -d " " -f 2)

export \
    AIRFLOW_HOME \
    AIRFLOW__CORE__EXECUTOR \
    AIRFLOW__CORE__SQL_ALCHEMY_CONN \
    AIRFLOW__CORE__FERNET_KEY \
    AIRFLOW__WEBSERVER__WORKERS \
    PIP_VERSION \

wait_for_port() {
    local name="$1" host="$2" port="$3"
    local j=0 TRY_LOOP=20
    while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
        j=$((j+1))
        if [ $j -ge $TRY_LOOP ]; then
            echo >&2 "$(date) - $host:$port still not reachable, giving up"
            exit 1
        fi
        echo "$(date) - waiting for $name... $j/$TRY_LOOP"
        sleep 5
    done
}

if [ $1 == "webserver" ]; then
    wait_for_port "MYSQL" "$MYSQL_HOST" "$MYSQL_PORT"
    airflow initdb
    airflow scheduler &
    exec airflow webserver -p 8080
fi

if [ $1 == "bash" ]; then
    exec /bin/bash
fi
