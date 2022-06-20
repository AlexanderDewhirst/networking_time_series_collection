# from functools import partial
# from bayes_opt import BayesianOptimization

import dotenv
from db import helpers as db
from services.detect import Detect

dotenv.load_dotenv()

if __name__ == "__main__":
  conn = db.create_connection('/Users/alexanderdewhirst/ports.db')

  detector = Detect(conn)
  detector()

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

# # def anomaly(self, timeseries_dataset, threshold=None):
# #   if threshold is not None:
# #     self.threshold = threshold

# #   dist = self.predict(timeseries_dataset)
# #   return zip(dist >= self.threshold, dist)
