# Contribute guide

## Stack

- [casey - just / github.com](https://github.com/casey/just) - like makefiles, but more convinient. Cli utility for management of project commands
- [Configuring Constraint Naming Conventions / docs.sqlalchemy.org](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)
- [Alembic Cookbook - Building an Up to Date Database from Scratch / alembic.sqlalchemy.org](https://alembic.sqlalchemy.org/en/latest/cookbook.html)
- [Alembic Cookbook - Integration of Naming Conventions into Operations, Autogenerate / alembic.sqlalchemy.org](https://alembic.sqlalchemy.org/en/latest/naming.html#integration-of-naming-conventions-into-operations-autogenerate)
- []()

- [?] - EdgeQL

## Installl developer environment

To simplify the environment, there are files: `.env`; `.dev.env`, `stage.env` and `.prod.env`.

- `.env` - uses just to load the environment

```conf
ENVIRONMENT=development

SECRET_KEY=asdgpjangi;adgjads;gja239htjpq9ghpjdgm398qrjgadkfjg
ENABLE_STATIC_FILES=True
```

## Code Convention

**Tags** in comments:

- `FIXME`: this works, sort of, but it could be done better.
- `TODO`: needs to be done.
- `NOTE`: code note that doesn't fit into docstring.
- `HACK`: (potential) vulnerability.
- `XXX`: warning about possible pitfalls.
- `BUG`: problem.
