import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from functools import partial
from bayes_opt import BayesianOptimization

from db import helpers as db
from models.cnn_rnn_ae import CnnRnnAe


conn = db.create_connection('/Users/alexanderdewhirst/ports.db')

rounds = db.select(conn, """SELECT id FROM rounds ORDER BY id DESC LIMIT 60;""")
rounds = tuple(map(lambda x: x[0], rounds))

port_usage = db.select(conn, "SELECT port_id, timestamp, round_id FROM rounds_ports WHERE round_id IN %s;", str(rounds))

def port_usage_per_round(port_usage):
  ports_per_round = [[] for r in rounds]

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

ports_per_round = port_usage_per_round(port_usage)
# pbounds = {
#   'conv_filters': (16, 32, 64),
#   'conv_kernel_size': (16, 64, 512),
#   'activation': 'relu',
#   'pool_size': (8, 32, 128),
#   'dropout': 0.05,
#   'lstm_nodes': 32,
#   'learning_rate': (0.001, 0.0001)
# }
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
model = CnnRnnAe()

# fit_with_partial = partial(model, pbounds)
# optimizer = BayesianOptimization(
#   f = fit_with_partial,
#   pbounds = pbounds,
#   verbose = 2
# )

# optimizer.maximize(init_points = 5, n_iter = 5,)

# for i, res in enumerate(optimizer.res):
#   print("Iteration {}: \n\t{}".format(i, res))

# print(optimizer.max)

# tf.keras.utils.plot_model(model, show_shapes = True)
# image = plt.imread('model.png')
# plt.imshow(image)
# plt.show()

ports_train, ports_test = train_test_split(ports_per_round, test_size = 0.2, train_size = 0.8)

early_stopping = tf.keras.callbacks.EarlyStopping(
  monitor = "val_loss",
  patience = 2,
  mode = "min"
)

model = model(ports_train, pbounds_default)
history = model.fit(
  ports_train,
  ports_train,
  epochs=20,
  batch_size=10,
  validation_data=(ports_test, ports_test),
  callbacks=[early_stopping]
)

print(history.history['loss'])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.xlabel('Epochs')
plt.ylabel('MSLE Loss')
plt.legend(['loss', 'val_loss'])
plt.show()

train_metrics = model.evaluate(ports_train, ports_train)
test_metrics = model.evaluate(ports_test, ports_test)

print(model.metrics_names)
print(train_metrics)
print(test_metrics)

# def find_threshold(model, x_train):
#   reconstructions = model.predict(x_train)
#   reconstruction_errors = tf.keras.losses.msle(reconstructions, x_train)
#   threshold = np.mean(reconstruction_errors.numpy()) \
#       + np.std(reconstruction_errors.numpy())
#   return threshold

# def get_predictions(model, x_test, threshold):
#   predictions = model.predict(x_test)
#   errors = tf.keras.losses.msle(predictions, x_test)
#   anomaly_mask = pd.Series(errors) > threshold
#   preds = anomaly_mask.map(lambda x: 0.0 if x == True else 1.0)
#   return preds

# threshold = find_threshold(model, ports_train)
# print(f"Threshold: {threshold}")
# errors = get_predictions(model, ports_test, threshold)
# print("Insample Error (MSLE): {}".format(errors))
# accuracy_score(predictions, ports_test)
