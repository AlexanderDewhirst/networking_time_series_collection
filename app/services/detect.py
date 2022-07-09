import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from datetime import datetime
from db import helpers as db
from models.cnn_lstm_ae import CnnLstmAe
from services.log import Log


class Detect():
  def __init__(self, conn, num_rounds = 60):
    self.conn = conn
    self.model = CnnLstmAe()
    self.model_file_path = CnnLstmAe.get_weight_file()
    self.num_rounds = num_rounds
    self.current_batch = self.__create_batch()

  def __call__(self):
    rounds = self.__get_rounds()
    self.__create_batch_rounds(rounds)

    Log("Batch " + str(self.current_batch) + " starting - rounds [" + str(rounds[-1]) + ' - ' + str(rounds[0]) + ']')

    port_usage = self.__get_port_usage(rounds)

    ports_per_round = self.port_usage_per_round(port_usage, rounds)

    # Create model
    self.build(ports_per_round)

    # Predict anomalies with trained model
    self.predict(ports_per_round)

    # Train model with latest weights
    self.train(ports_per_round)

  @staticmethod
  def port_usage_per_round(port_usage, rounds):
    ports_per_round = [[] for _ in rounds]

    # Create array of unique ports per round
    for record in port_usage:
      idx = record[2] - rounds[0]
      if record[0] not in ports_per_round[idx]:
        ports_per_round[idx].append(record[0])

    # Assign value given port usage during round
    for i in range(len(ports_per_round)):
      ports = ports_per_round[i]
      all_ports = [0] * 65535
      for port in ports:
        all_ports[port] = 1
      ports_per_round[i] = all_ports

    ports_per_round = np.vstack(ports_per_round)
    return ports_per_round

  def build(self, ports_per_round):
    if os.path.exists(self.model_file_path):
      model_file = self.model_file_path
    else:
      model_file = None

    pbounds_default = {
      'conv_filters': 32,
      'conv_kernel_size': 128,
      'activation': 'relu',
      'pool_size': 32,
      'dropout': 0.05,
      'lstm_nodes': 32,
      'ae_code_size': 16,
      'learning_rate': 0.001
    }
    self.model.set_model_file(model_file)
    self.model = self.model(ports_per_round, pbounds_default)

  def predict(self, ports_per_round):
    Log("Batch " + str(self.current_batch) + " predicting anomalies")
    pred = self.model.predict(ports_per_round)
    mae_loss = np.mean(np.abs(pred - ports_per_round), axis = 1)
    threshold = np.max(mae_loss)
    Log("Reconstruction error threshold: " + str(threshold))
    Log(list(zip(mae_loss >= threshold, mae_loss)))

  def train(self, ports_per_round):
    ports_train, ports_test = train_test_split(ports_per_round, test_size = 0.2, train_size = 0.8)

    early_stopping = tf.keras.callbacks.EarlyStopping(
      monitor = "val_loss",
      patience = 2,
      mode = "min"
    )
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
      filepath = self.model_file_path,
      save_weights_only = True,
      verbose = 1
    )

    Log("Batch " + str(self.current_batch) + " fitting")
    self.model.fit(
      ports_train,
      ports_train,
      epochs = 20,
      batch_size = 10,
      validation_data = (ports_test, ports_test),
      callbacks = [early_stopping, model_checkpoint]
    )
    self.model.save(self.model_file_path)

  def plot_history(self, history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.xlabel('Epochs')
    plt.ylabel('MSLE Loss')
    plt.legend(['loss', 'val_loss'])
    plt.show()

  def plot_loss(self, mae_loss):
    plt.hist(mae_loss, bins = 50)
    plt.xlabel("Train MAE Loss")
    plt.ylabel("Sample Size")
    plt.show()

  def plot_model(self):
    tf.keras.utils.plot_model(self.model, show_shapes = True, to_file = 'model.png')
    image = plt.imread('model.png')
    plt.imshow(image)
    plt.show()

  def __get_rounds(self):
    # Check batches_rounds. Must ensure uniqueness for processed rounds in each batch.
    rounds = db.select(self.conn, """SELECT id FROM rounds ORDER BY id DESC LIMIT %s;""", str(self.num_rounds))
    rounds = tuple(map(lambda x: x[0], rounds))

    processed_rounds = db.select(self.conn, """SELECT round_id FROM batches_rounds WHERE round_id IN %s;""", str(rounds))
    processed_rounds = list(map(lambda x: x[0], processed_rounds))
    new_rounds = []
    for round in list(rounds):
      if round not in processed_rounds:
        new_rounds.append(round)
    return tuple(new_rounds)

  def __get_port_usage(self, rounds):
    return db.select(self.conn, "SELECT port_id, timestamp, round_id FROM rounds_ports WHERE round_id IN %s;", str(rounds))

  def __create_batch(self):
    # TODO: API request
    #   BatchService - POST /projects/{id}/batches
    insert_batch_query = """INSERT INTO batches(timestamp, alg) VALUES (?, ?);"""
    db.insert(self.conn, insert_batch_query, (datetime.now().isoformat(), self.model.__name__()))

    select_batch_query = """SELECT id FROM batches ORDER BY id DESC LIMIT 1;"""
    current_batch = db.select(self.conn, select_batch_query)[0][0]
    return str(current_batch)

  def __create_batch_rounds(self, rounds):
    rounds_params = []
    for round in rounds:
      rounds_params.append((
        self.current_batch,
        str(round)
      ))

    # TODO: Handled by BatchService - on create_batch
    insert_batch_rounds_query = """INSERT INTO batches_rounds(batch_id, round_id) VALUES (?, ?);"""
    db.insert_many(self.conn, insert_batch_rounds_query, rounds_params)
