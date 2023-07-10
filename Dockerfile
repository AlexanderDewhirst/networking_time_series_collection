FROM ubuntu:20.04

ENV PYTHONPATH "${PYTHONPATH}:/usr/bin"

WORKDIR /
COPY /app /

# Install Dependencies
RUN apt-get update
RUN apt-get install -y \
    sqlite3 \
    cron \
    nano \
    software-properties-common

# Install Python & Pip
RUN apt-get install python3.9 --assume-yes
RUN apt-get install python3-pip --assume-yes

# Initialize Database
RUN sqlite3 -init init.sql ports.db ""

# Install Python Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --default-timeout=1000 -r requirements.txt

RUN python3 db/reset.py

# Setup executables
RUN chmod +x port_collector.py
RUN chmod +x port_detector.py
RUN chmod +x port_cleanup.py

# Create log files
RUN touch collector.log
RUN touch detector.log

RUN crontab -e | { cat; echo \
"*/1 * * * * /usr/bin/python3 /port_collector.py -d /ports.db -r 60 >> /collector.log 2>&1 \
\n0 * * * * /usr/bin/python3 /port_detector.py -d /ports.db -r 60 >> /detector.log 2>&1 \
\n0 0 * * * /usr/bin/python3 /port_cleanup.py -d /ports.db\n"; \
} | crontab -

# Run cron on container startup
CMD service cron start & tail -f collector.log
