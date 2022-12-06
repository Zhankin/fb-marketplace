# Python Base Image
FROM python:3.9-alpine
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

# Creating Working
WORKDIR /py_cronjob

# Install chromedriver
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update
RUN apk add chromium
RUN apk add chromium-chromedriver

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --default-timeout=180
RUN pip3 install urllib3==1.24.1 
# Copying the crontab file
COPY crontab /etc/cron.d/crontab
# Copy the each file from docker_py_project to py_cronjob in docker container
COPY . .

# run the crontab file
RUN crontab /etc/cron.d/crontab

# Executing crontab command
CMD ["crond", "-f"]
