import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

data = pd.read_csv('port_usage.csv')
port_usage_df = pd.DataFrame(data, columns = [
  'timestamp',
  'protocols',
  'srcport',
  'dstport',
  'qry_name',
  'resp_name',
  'payload'
])

print(port_usage_df.columns)
print(port_usage_df.head())

port_usage_train_df, port_usage_test_df = train_test_split(port_usage_df, test_size = 0.2)

print(port_usage_train_df.columns)

# protocol_encoder = OneHotEncoder()
# protocol_encoder = protocol_encoder.fit([port_usage_train_df['protocols']])

# port_usage_train_df.drop('protocols', axis = 1, inplace = True)
# port_usage_train_df = port_usage_train_df.join(protocol_encoder.transform[port_usage_train_df['protocols']])
# port_usage_test_df.drop('protocols', axis = 1, inplace = True)
# port_usage_test_df = port_usage_test_df.join(protocol_encoder.transform(port_usage_test_df['protocols']))

# print(port_usage_train_df.head())
# print(port_usage_test_df.head())

src_port_one_hot = pd.get_dummies(port_usage_train_df.srcport, prefix = 'src', dtype = int)
port_usage_train_df.drop('srcport', axis = 1, inplace = True)
port_usage_train_df = port_usage_train_df.join(src_port_one_hot)

dst_port_one_hot = pd.get_dummies(port_usage_train_df.dstport, prefix = 'dst', dtype = int)
port_usage_train_df.drop('dstport', axis = 1, inplace = True)
port_usage_train_df = port_usage_train_df.join(dst_port_one_hot)

print(port_usage_train_df.describe())
print(port_usage_train_df.head())
print(port_usage_train_df.columns)
print(port_usage_train_df.shape)

import seaborn as sns
import matplotlib.pyplot as plt

# sns.distplot(port_usage_df['protocol'])
# plt.show()

import tensorflow as tf

cols = len(port_usage_train_df.columns)

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(cols))
# TODO: Check port batches
model.add(tf.keras.layers.Conv1D(8, 10, padding = 'same', activation = 'relu'))
model.add(tf.keras.layers.Conv1D(4, 5, padding = 'same', activation = 'relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy', metrics = ['mae', 'acc'])
print(model.summary())

model.fit(port_uaage_train_df, port_usage_test_df, epochs = 5, validation_data =)
