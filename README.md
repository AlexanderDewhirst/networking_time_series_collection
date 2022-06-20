# Port Consumption Anomaly Detector Client using CNN-LSTM-AE (Neural Network) Architecture

## Introduction
This application collects local port and network packet time series data, stores the data on the client, and evaluates anomalies using cron while the host machine is active.


## Architecture
The application collects network traffic and detects anomalies in port occupancy using cron jobs.

The network traffic collector scans for port occupancy and streams network packets on the `en0` interface. Jobs run every minute, with each storing port usage and network packets in an in-process database. For each round, two classes overriding an instance of `threading.Thread` in the directory `/threads` (`ScannerThread` and `SnifferThread`) are called. These call the respective services in directory `/services` (`Scanner` and `Sniffer`). Each Thread class then stores the data in the SQLite3 database.

<p align='center'>
  ![Client - Collector](/docs/collector.png)
</p>

The anomaly detector runs every hour and predicts anomalies within batched time series data using a convolutional neural network (CNN), a recurrent neural network (RNN), and an autoencoder (AE). The CNN extracts local features in port usage. The RNN, which uses Long Short-Term Memory (LSTM) network, extracts temporal features in port usage. Finally, the AE compresses and decompresses the data in order to generalize features to detect anomalies for unlabeled data. For each batch, the `keras.engine.Sequential` model stored on the client predicts anomalies by using the reconstruction threshold from the undercomplete autoencoder and then refits with the data after evaluation, preserving the temporality of time series data and maintaining the model weights.

<p align='center'>
  ![Client - Detector](/docs/detector.png)
</p>

The neural network model architecture uses Keras high-level API to construct layers. The first layer is an input layer followed by a 1-dimensional convolutional layer with the shape defined as the port input space (1 x 65535). A 1-dimensional maximum pooling layer then compresses the local features into a lower dimensional space. Dropout is added to further allow our model to generalize local features. An LSTM layer then allows for our model to realize temporal features in the data. Lastly, we have two dense layers to compress and decompress the data, implementing an under-complete autoencoder, to further generalize and label anomalous behavior.

<p align='center'>
  ![Model Architecture](/docs/model_architecture.png)
</p>

The database consists of four tables: _rounds_, _ports_, _packets_, and _rounds_ports_. This allows for port status data to belong to a particular round for a client, supporting federation. The network packet data also belongs to a particular port and a particular round, associating packets to specific ports and supporting federation.

<p align='center'>
  ![Database](/docs/database_design.png)
</p>

- Rounds ( id, start_time )
- Ports ( id, value )
- RoundsPorts ( id, round_id, port_id, timestamp )
- Packets ( id, timestamp, protocols, qry_name, resp_name, port_id, dest_port, payload, round_id )
<!-- Separate Packet record per protocol -->


## Getting Started - Host Machine
Clone the repository and navigate to the directory of choice and install the dependencies with:
```
pip3 install -r requirements.txt
```

### SQLite Initialization
To initialize the SQLite3 database, execute the following:
```
sqlite3 -init init.sql ~/ports.db ""
```

Unfortunately, SQLite does not support native variable syntax. Therefore, seeding the database is done at the application layer.
```
python3 ~/<path_to_repository>/app/db/reset.py
```

### Cronjob Scheduling
Setup a cronjob with:
```
crontab -e
```
and use the following syntax to schedule the job. Cron requires the global path to find the file.
```
*/1 * * * * python3 app/port_collector.py
0 * * * * python3 app/port_detector.py
```
and both files are executable (ex. `chmod +x app/port_collector.py`). 

We must also give cron full disk access - osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/

##### NOTES
1. The cron job will initialize the database at the root. See *dependencies* for accessing the database console.
2. You will likely need to configure cron to use the correct installation of Python. You can swap out `python3` with the result of `which python3`.
3. The logs from the cron execution can be saved in a log file with the following syntax
```
python3 app/port_collector.py >> collector.log 2>&1
```
The files `collector.log` and `detector.log` are ignored from Git for this purpose.
4. Configuration of the PATH environment variable to allow cron to use the latest version of Python might be required. The Live Capture functionality from `pyshark` requires a recent version of Python and PIP.
5. The application will execute without Wireshark and the Sniffer thread streaming network packets to the database. However, we can configure Wireshark to allow execution by cron by modifying the file `dumpcap` path in `config.ini` for `pyshark` within your current Python dependencies (ex. `/usr/local/lib/python3.9/site-packages/pyshark`). The dumpcap path should point to your TShark installation (ex. `dumpcap_path = /Applications/Wireshark.app/Contents/MacOS/tshark`)


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

### Python Dotenv
The Python library `python-dotenv` loads environment variables necessary for development.

## Future State
### Federation
Develop a server application to support federation and manage client participation in the neural network usage (training and evaluation), aggregating weights from the client models at time t + 1 using Stochastic Parallel Gradient Descent (SPGD).

### Bayesian Optimization
Tune model hyperparameters to optimize our model performance.

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
