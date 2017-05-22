# bugbuzz-api
Bugbuzz HTTP API server

# Setup development environment

Clone bugbuz API repo, cd to the folder, then install the dependencies

```bash
pip install -e.[tests]
```

Ensure you have PostgreSQL running and have `bugbuzz` database, then run

```bash
bugbuzz_service -c development.ini initdb
```

to create tables. Next, you can now run the server, via

```bash
pserve development.ini
```

For now, the API server should be up and running. If you have different database configuration, you can modify `development.ini` and change `sqlalchemy.url = postgres://localhost/bugbuzz` to something else.

# Relative projects

 - [Ember.js Dashboard project](https://github.com/victorlin/bugbuzz-dashboard)
 - [Python debugger library project](https://github.com/victorlin/bugbuzz-python)
 
