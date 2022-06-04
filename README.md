# Client Data Collection

## Introduction
This application collects local port and network packet time series data and stores the data locally. With a Cronjob, the data is collected while the computer is unlocked and active.


## Getting Started
Clone the repository and navigate to the directory of choice and install the dependencies with:
```
pip3 install -r requirements.txt
```
This requires Wireshark to be installed as well.

### SQLite Initialization
To initialize the SQLite3 database, execute the following:
`sqlite3 -init ~/<path_to_repository>/init.sql ports.db ""`

Unfortunately, SQLite does not support native variable syntax. Therefore,eeding the database is done at the application layer.
<!-- Seed DB -->

### Cronjob Scheduling
Setup a cronjob with:
```
crontab -e
```
and use the following syntax to schedule the job:
```
*/1 * * * * ~/<path_to_repository>/run.sh
```
and ensure the `run.sh` file is executable (`chmod 777 run.sh`)


## Architecture
The application consists of a Python script which is scheduled regularly to collect port occupancy and network packet time series data. Each job starts a new round, effectively batching the collected time series data. For each round, two classes overriding an instance of `threading.Thread` in the directory `/threads` {`ScannerThread` and `SnifferThread`} are called. These call the respective services in directory `/services` (`scanner` and `Sniffer`). Each Thread class then stores the data in the SQLite3 database.


## Dependencies
### PyShark
The Python library `pyshark` is used to sniff packets with LiveCapture. The capture packets include protocols TCP, DNS, QUIC, and UDP on the `en0` interface.

### Threading
The Python library `threading` manages concurrency within the application. Two threads are initialized to scan ports and sniff packets continuously.

### Sockets
The Python library `sockets` is used to bind to local ports and determine the port occupancy. Sockets is installed with the standard Python library

### SQLite3
A lightweight, in process database to store data on the client. SQLite3 is installed with the standard Python library.

To access the SQLite console, simply connect to the database with:
`sqlite3 ports.db`

- `.tables` - List tables
- `.mode list` - Set display mode
