#!/bin/bash


AIRFLOW__CORE__FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")

export \
    AIRFLOW_HOME \
    AIRFLOW__CORE__EXECUTOR \
    AIRFLOW__CORE__SQL_ALCHEMY_CONN \
    AIRFLOW__CORE__FERNET_KEY \


wait_for_port() {
    local name="$1" host="$2" port="$3"
    local j=0
    local TRY_LOOP=20
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
    sleep 10
    airflow schedular &
    airflow webserber -p 8080
fi

if [ $1 == "worker" ]; then
    echo $1
fi

if [ $1 == "bash" ]; then
    wait_for_port "MYSQL" "$MYSQL_HOST" "$MYSQL_PORT"
    exec /bin/bash
fi
