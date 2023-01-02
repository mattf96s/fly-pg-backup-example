# pg-backup

Cron job to backup fly database and upload to S3.

## Inspiration

[Based on this tutorial](https://www.advantch.com/blog/automate-postgres-database-backups-on-fly-dot-io/)

> Why is this in python? because the tutorial is.

## Setup

For Local Testing:
Ensure Postgres is setup correctly (especially the path)

```
sudo mkdir -p /etc/paths.d && echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
```

Create and activate a virtual env
Run in the terminal in the following order:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt
```

## Problem Solving

> note the naming inconsitencies between hyphens and underscores.

How do I even get the various connection values?

```
flyctl ssh console -a my-remix-app-34bb-staging
```

```
echo $DATABASE_URL
```

Connection to DB often hangs when testing locally--so need to [kill it.](https://stackoverflow.com/questions/20091433/cant-find-out-where-does-a-node-js-app-running-and-cant-kill-it)

```
lsof -i tcp:5432
kill xxx
```
