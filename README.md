# Combot

Originally written by @japroc (https://gitlab.com/japroc/combot)

## Deployment

1. `cp example.env .env` and put the credentials there
2. `docker compose up --build -d`

Or just build an image and run it with `docker run` with envvars from `example.env`

### Obsolete Heroku method

Originally, the bot was hosted on Heroku free plan, but they are not so generous anymore. If for some reason
you still want to read the original "Heroku Free Plan" deployment guide, see the commit history for README.
