###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.3-alpine as builder

# set work directory
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc musl-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . .



# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3-alpine

# create directory for the app user
RUN mkdir -p /home/app


# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME
RUN apk add --update tzdata
ENV TZ=Asia/Calcutta


# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN apk update \
    && apk add postgresql-dev gcc musl-dev
RUN pip install --no-cache /wheels/*
RUN pwd
RUN ls -a

# copy project
COPY . $APP_HOME


# chown all the files to the app user
RUN chown -R app:app $APP_HOME
# change to the app user
USER app

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
