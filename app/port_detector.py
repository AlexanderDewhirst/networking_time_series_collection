from functools import partial
from bayes_opt import BayesianOptimization

from db import helpers as db
from services.detect import Detect


if __name__ == "__main__":
  conn = db.create_connection('/Users/alexanderdewhirst/ports.db')

  detector = Detect(conn)
  detector()

# rounds = db.select(conn, """SELECT id FROM rounds ORDER BY id DESC LIMIT 60;""")
# rounds = tuple(map(lambda x: x[0], rounds))

# port_usage = db.select(conn, "SELECT port_id, timestamp, round_id FROM rounds_ports WHERE round_id IN %s;", str(rounds))

# def port_usage_per_round(port_usage):
#   ports_per_round = [[] for r in rounds]

#   # Create array of unique ports per round
#   for record in port_usage:
#     idx = record[2] - rounds[0]
#     if record[0] not in ports_per_round[idx]:
#       ports_per_round[idx].append(record[0])

#   # Assign value given port usage during round
#   for i in range(len(ports_per_round)):
#     ports = ports_per_round[i]
#     all_ports = [0] * 65535
#     for port in ports:
#       all_ports[port] = 1
#     ports_per_round[i] = all_ports

#   ports_per_round = np.vstack(ports_per_round)
#   return ports_per_round

# ports_per_round = port_usage_per_round(port_usage)
# # pbounds = {
# #   'conv_filters': (16, 32, 64),
# #   'conv_kernel_size': (16, 64, 512),
# #   'activation': 'relu',
# #   'pool_size': (8, 32, 128),
# #   'dropout': 0.05,
# #   'lstm_nodes': 32,
# #   'learning_rate': (0.001, 0.0001)
# # }
# pbounds_default = {
#   'conv_filters': 32,
#   'conv_kernel_size': 128,
#   'activation': 'relu',
#   'pool_size': 32,
#   'dropout': 0.05,
#   'lstm_nodes': 32,
#   'ae_code_size': 16,
#   'learning_rate': 0.001
# }
# model = CnnRnnAe()

# # fit_with_partial = partial(model, pbounds)
# # optimizer = BayesianOptimization(
# #   f = fit_with_partial,
# #   pbounds = pbounds,
# #   verbose = 2
# # )

# # optimizer.maximize(init_points = 5, n_iter = 5,)

# # for i, res in enumerate(optimizer.res):
# #   print("Iteration {}: \n\t{}".format(i, res))

# # print(optimizer.max)

# ports_train, ports_test = train_test_split(ports_per_round, test_size = 0.2, train_size = 0.8)

# early_stopping = tf.keras.callbacks.EarlyStopping(
#   monitor = "val_loss",
#   patience = 2,
#   mode = "min"
# )

# model = model(ports_train, pbounds_default)

# history = model.fit(
#   ports_train,
#   ports_train,
#   epochs=20,
#   batch_size=10,
#   validation_data=(ports_test, ports_test),
#   callbacks=[early_stopping]
# )

# # print(history.history['loss'])

# ports_train_pred = model.predict(ports_train)
# train_mae_loss = np.mean(np.abs(ports_train_pred - ports_train), axis = 1)

# # plt.hist(train_mae_loss, bins = 50)
# # plt.xlabel("Train MAE Loss")
# # plt.ylabel("Sample Size")
# # plt.show()

# threshold = np.max(train_mae_loss)
# print("Reconstruction error threshold: ", threshold)

# # plt.plot(ports_train[0])
# # plt.plot(ports_train_pred[0])
# # plt.show()

# # Look into np.save

# # Cron every hour
# #
# # Pull last 60 minutes
# # Test against trained model from file weights
# #   IF no model -> train model. write to file weights
# #   IF model -> detect anomalies. update file weights


# # def get_weight_file(model_dir_path):
# #   return model_dir_path + '/' + CnnRnnAe.model_name + '-weights.h5'

# # def get_config_file(model_dir_path):
# #   return model_dir_path + '/' + CnnRnnAe.model_name + '-config.npy'

# # def get_architecture_file(model_dir_path):
# #   return model_dir_path + '/' + CnnRnnAe.model_name + '-architecture.json'

# # def anomaly(self, timeseries_dataset, threshold=None):
# #   if threshold is not None:
# #     self.threshold = threshold

# #   dist = self.predict(timeseries_dataset)
# #   return zip(dist >= self.threshold, dist)
