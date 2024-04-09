FROM python:3.6-alpine
WORKDIR /app
# Add requirements first to avoid rebuilding dependencies each time something but requirements changes
ADD ./app/requirements.txt /app
RUN apk add --update build-base postgresql-libs postgresql-dev linux-headers
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apk del build-base postgresql-dev linux-headers

ADD ./app /app
ADD ./runner.py /runner.py
RUN chmod 755 /app/scripts/start_bot.sh
