# Port Consumption Anomaly Detector Client using CNN-LSTM-AE (Neural Network) Architecture

## Introduction
This application collects local port and network packet time series data and stores the data locally. The data is collected using a cron job while the host machine is active.


## Architecture
The application includes both a network traffic data collection phase and a neural network anomaly detection phase.

The data collection phase collects port occupancy and network packet time series data. Each job starts a new round, effectively batching the collected time series data.

The anomaly detection phase predicts anomalies within batched time series data using a convolutional neural network (CNN), a recurrent neural network (RNN), and an autoencoder (AE). The CNN extracts local features in port usage. The RNN, which uses Long Short-Term Memory (LSTM) network, extracts temporal features in port usage. Finally, the AE compresses and decompresses the data in order to generalize features to detect anomalies for unlabeled data. After evaluating the latest batch using the current weights, the model is further trained using the data for evaluation in the next batch.

### Data Structure
Rounds ( id, start_time )

Ports ( id, value )

RoundsPorts ( id, round_id, port_id, timestamp )

Packets ( id, timestamp, protocols, qry_name, resp_name, port_id, dest_port, payload, round_id )
<!-- Separate Packet record per protocol -->


## Architecture
Two executable scripts to collect network traffic and evaluate port occupancy are scheduled using cron.

The script to collect network traffic runs every minute, and stores port usage and network packets in an in-process database. For each round, two classes overriding an instance of `threading.Thread` in the directory `/threads` (`ScannerThread` and `SnifferThread`) are called. These call the respective services in directory `/services` (`Scanner` and `Sniffer`). Each Thread class then stores the data in the SQLite3 database.

The script to evaluate port occupancy runs every hour, evaluating the latest port usage data using a CNN-LSTM-AE neural network. For each batch, the `keras.engine.Sequential` model stored on the client predicts anomalies by using the reconstruction threshold from the undercomplete autoencoder and then refitted with the data after evaluation, preserving the temporality of time series data and maintaining the model weights.

## Getting Started - Host Machine
Clone the repository and navigate to the directory of choice and install the dependencies with:
```
pip3 install -r requirements.txt
```
This requires Wireshark to be installed as well.

Currently, Wireshark is a required dependency and must be installed. To configure Wireshark to allow execution by cron, we have to modify the file `config.ini` in the Wireshark `sitepackages` by adding the correct Python path.

### SQLite Initialization
To initialize the SQLite3 database, execute the following:
```
sqlite3 -init init.sql ports.db ""
```

Unfortunately, SQLite does not support native variable syntax. Therefore, seeding the database is done at the application layer.
```
python3 app/db/reset.py
```

### Cronjob Scheduling
Setup a cronjob with:
```
crontab -e
```
and use the following syntax to schedule the job:
```
*/1 * * * * python3 app/port_collector.py
0 * * * * python3 app/port_detector.py
```
and both files are executable (`chmod +x app/port_collector.py`).

##### NOTES
1. The cron job will initialize the database at the root. See *dependencies* for accessing the database console.
2. Configuration of the PATH environment variable to allow cron to use the latest version of Python might be required. The Live Capture functionality from `pyshark` requires a recent version of Python and PIP.


## Getting Started - Docker (WIP)
Clone the repository and navigate to the directory of choice. Build the docker image with
```
docker build -t port_monitor .
```

We can then start the container using out new image with
```
docker run -it -d --net=host port_monitor
```

##### LIMITATIONS
1. Mapping the network from the host machine is not supported by Windows.
2. Installing Wireshark is required on the host machine. Only Linux allows commands from the Dockerfile to setup Wireshark on the host. This will not be supported.


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

### Numpy
The Python library `numpy` is used to preprocess the stored data into an acceptable data structure for the neural network model.

### Tensorflow
The Python library `tensorflow` is required to construct the neural network model.

### Scikit-Learn
The Python library `scikit-learn` allows us to split the data into training and testing datasets.

### Matplotlib
The Python library `matplotlib` is a plotting library that allows us to visualize our model and data.

## Future State
### Federation
Develop a server application to support federation and manage client participation in the neural network usage (training and evaluation), aggregating weights from the client models at time t + 1 using Stochastic Parallel Gradient Descent (SPGD).

### Data Cleanup Worker
Data is retained indefinitely on the host machine (unless the database process is killed) and should be removed after considered stale.

### CLI
Create a CLI tool to allow for specific use cases.

### Data Security
Use and secure credentials for the client application to write to the database on the host machine.

### Packets
Use the data to help predict anomalies!

## Other Ideas
### Generative Adversarial Networks (GANs)
One interesting project would be to train a GAN to fake port activity. This could be useful in testing load capacity in cloud environments.
