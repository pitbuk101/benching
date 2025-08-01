# Use the official PostgreSQL 15 image
FROM postgres:15

# Set environment variables (can be overridden in docker-compose.yml)
ENV POSTGRES_DB=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Install pgvector extension
RUN apt-get update && apt-get install -y postgresql-contrib && \
    apt-get install -y postgresql-server-dev-15 && \
    apt-get install -y gcc make && \
    apt-get install -y git && \
    git clone --depth 1 --branch v0.5.1 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && make install && \
    cd .. && rm -rf pgvector && \
    apt-get remove -y git gcc make postgresql-server-dev-15 && \
    apt-get autoremove -y && \
    apt-get clean

# Copy initialization scripts (if needed)
# COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432