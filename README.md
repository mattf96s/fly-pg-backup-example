# Automated Fly.io Postgres Database Backups

An example showing how to use a GitHub action to automate backups of a Fly.io Postgres database as well as then uploading the backups to S3 (or another storage provider of your choosing).

## Quick Start

Clone this repo and add your environment variables as secrets to your GitHub action.

- Control the cron frequency in the backup.yml file
  </br>

## Recognition

This example is based on the following [tutorial](https://www.advantch.com/blog/automate-postgres-database-backups-on-fly-dot-io/) by <i>advantch</i>. However, there were certain steps which were unclear to me—as someone with relatively little python or bash knowledge.

I also find the Fly naming conventions confusing—particularly between the switching of hyphens and underscores in app names. This made the tutorial harder to follow and I thought it was worth sharing for others.
</br>

## A Simple Explanation

We proxy our Postgres app to port 5432 and then perform usual pg_dump commands.

## Setting up your environment variables

Add the following environment variables to your GitHub action secrets.

For illustration purposes, assume my main fly app is called `my-example-app` and my attached Postgres fly app is called `my-example-app-db`.

</br>

> 💡 How to find some of these values is explained further down.

</br>
<i>Fly.io specific variables</i>

|                | Example           | Explanation                    |
| -------------- | ----------------- | ------------------------------ |
| PG_PASSWORD    |                   |                                |
| PG_USER        | my_example_app    | Note the underscores           |
| PG_DATABASE    | my_example_app    | Note the underscores           |
| APP_NAME       | my-example-app    | main fly app name              |
| PROXY_APP_NAME | my-example-app-db | attached fly Postgres app name |

</br>
<i>S3 specific variables</i>

|                      | Example             | Explanation |
| -------------------- | ------------------- | ----------- |
| S3_ACCESS_KEY        |                     |             |
| S3_SECRET_ACCESS_KEY |                     |             |
| S3_BUCKET            | my-database-backups |             |
| AWS_REGION           | eu-west-1           |             |

### How to retrieve certain environment values

> Ensure that you are logged into your fly account:

```
flyctl auth login
```

### Retrieving Your App Names

```
flyctl list apps
```

### Retrieving your Postgres Users

```
fly postgres users list -a my-example-app-db
```

### Retrieving the Postgres specific values

For your app name, do not use the Postgres app name; instead, it needs to be the app to which the PostGres app is attached. If you omit the -a flag it will use the app specified in your fly.toml file—which is usually what we want anyway.

```
flyctl ssh console -a my-example-app
```

```
echo $DATABASE_URL
```

You can also see all variables with

```
printenv
```

Again, assuming my main fly app is called `my-example-app` and my postgres fly app is called `my-example-app-db`.

Your `DATABASE_URL` should look something like: `postgres://my_example_app:Rhakkai12jsjs@top2.nearest.of.my-example-app-db.internal:5432/my_example_app?sslmode=disable`

> 💡 postgres://{username}:{password}@{hostname}:{port}/{database}?options

[Learn more here](https://fly.io/docs/postgres/connecting/connecting-internal/)

What is confusing is when to use hyphens and when to use underscores.

It helps to remember that "Fly Postgres is a regular app". So we need to differentiate between the naming of the Fly app hosting the Postgres database to that of the actual database itself.

## For Local Testing:

Ensure Postgres is setup correctly (especially the path)

```
sudo mkdir -p /etc/paths.d && echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
```

Create and activate a virtual environment.

Run the following lines of code in your terminal:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt
```

The connection to DB often hangs when testing locally--so you may need to [kill it](https://stackoverflow.com/questions/20091433/cant-find-out-where-does-a-node-js-app-running-and-cant-kill-it).

```
lsof -i tcp:5432
kill xxx
```
