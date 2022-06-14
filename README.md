# Client Application

## Introduction
This application collects local port and network packet time series data and stores the data locally. The data is collected using a cron job while the host machine is active.


## Architecture
The application includes both a data collection phase and neural network modeling phase: 

The data collection phase consists of a Python script which is scheduled regularly to collect port occupancy and network packet time series data. Each job starts a new round, effectively batching the collected time series data. For each round, two classes overriding an instance of `threading.Thread` in the directory `/threads` {`ScannerThread` and `SnifferThread`} are called. These call the respective services in directory `/services` (`scanner` and `Sniffer`). Each Thread class then stores the data in the SQLite3 database.

The neural network modeling phase uses a convolutional neural network (CNN), a recurrent neural network (RNN), and an autoencoder (AE). The CNN extracts local features in port usage. The RNN, which uses Long Short-Term Memory (LMTM) network, extracts temporal features in port usage. Finally, the AE compresses and decompresses the data in order to generalize features to detect anomalies for unlabeled data.


### Date Structure
Rounds ( id, start_time )
Ports ( id, value )
RoundsPorts ( id, round_id, port_id, timestamp )
Packets ( id timestamp, protocols, qry_name, resp_name, port_id, dest_port, payload, round_id )
<!-- Separate Packet record per protocol -->


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


## Future State

### Docker
Package the client application in a Docker container for the ability to run on any operating system. This would require mapping all ports from the host machine to the container, executing the cron job within the container, and storing data within a database in the container. Required dependencies installed in the container include the libraries above plus Wireshark.


### Server Application
Develop a server application to manage client participation in the neural network usage (training and evaluation), aggregating weights from the client models at time t + 1 using Stochastic Parallel Gradient Descent (SPGD).


### Data Cleanup Worker
Data is retained indefinitely on the host machine (unless the database process is killed) and should be removed after considered stale.


### Packets
Use the data to help predict anomalies!


## Other Ideas
### Generative Adversarial Networks (GANs)
One interesting project would be to train a GAN to fake port activity. This could be useful in testing load capacity in cloud environments.
