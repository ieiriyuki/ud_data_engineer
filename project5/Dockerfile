FROM apache/airflow:master

RUN pip install -U --user pip

COPY . .

EXPOSE 8080

ENTRYPOINT [ "./entrypoint.sh" ]

CMD [ "bash" ]
