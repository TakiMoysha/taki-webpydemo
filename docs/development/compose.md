## Networks

Сеть делится на `private.net` и `gateway.net`.

**private.net** содержит службы/сервсы которые не должны быть доступны из вне. БД, кэш, брокеры, proxy и т.д.
**gateway.net** содержит разрабатываемые сервисы.

## Examples

### Persistance Layer

**DBeaver**:

```yaml
dbeaver:
  image: dbeaver/dbeaver
  ports:
    - 8080:8080
  networks:
    - private.net
    - gateway.net
```

**adminer**:

- supports: MySQL, MariaDB, PostgreSQL, CockroachDB, SQLite, MS SQL, Oracle
- plugins for: Elasticsearch, SimpleDB, MongoDB, Firebird, ClickHouse, IMAP
- sources: PHP

```yaml
adminer:
  image: adminer
  ports:
    - 8081:8080
  networks:
    - private.net
    - gateway.net
```

**pgadmin**:

- supports: PostgreSQL
- sources: python, nodejs

```yaml
pgadmin:
image: dpage/pgadmin4
environment:
  - PGADMIN_DEFAULT_EMAIL=
  - PGADMIN_DEFAULT_PASSWORD=
  - PGADMIN_CONFIG_SERVER_MODE=
ports:
  - 8082:80
networks:
  - private.net
  - gateway.net
```

**mongodb**:

```yaml
mongodb:
  image: mongodb/mongodb-community-server
  environment:
    - MONGODB_INITDB_ROOT_USERNAME=
    - MONGODB_INITDB_ROOT_PASSWORD=
  ports:
    - 27017:27017
  networks:
    - private.net
  volumes:
    - database-volume:/data/db
```

### 3rd party services

**mailhog**:

```yaml
mailhog:
  image: mailhog/mailhog
  ports:
    - 8025:8025
  networks:
    - private.net
    - gateway.net
```
