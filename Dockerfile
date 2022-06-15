FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install software-properties-common --assume-yes
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.9 --assume-yes
RUN apt-get install python3-pip --assume-yes

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

# Give execution rights on the cron scripts
RUN chmod 777 ubuntu.sh

# Install Cron
RUN apt-get -y install cron

RUN touch foo.log
RUN echo "ALEX"
RUN crontab -e | { cat; echo "* * * * * root echo 'Hello world' >> foo.log 2>&1"; } | crontab -
RUN crontab -e | { cat; echo "*/1 * * * * bash ubuntu.sh >> foo.log 2>&1"; } | crontab -

# Run the command on container startup
CMD cron && tail -f foo.log
