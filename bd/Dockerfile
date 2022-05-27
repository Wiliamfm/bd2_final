FROM postgres
COPY ./billing.sql ./docker-entrypoint-initdb.d/1.sql
COPY ./billing_inserts.sql ./docker-entrypoint-initdb.d/2.sql
EXPOSE 5432
ENV POSTGRES_DB=bills
ENV POSTGRES_PASSWORD=1234
CMD postgres