# Python Base Image
FROM python:3.10-alpine

# Creating Working
WORKDIR /py_cronjob

# Copying the crontab file
COPY crontab /etc/cron.d/crontab
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --default-timeout=180

# Copy the each file from docker_py_project to py_cronjob in docker container
COPY . .

# run the crontab file
RUN crontab /etc/cron.d/crontab

# Executing crontab command
CMD ["cron", "-f"]