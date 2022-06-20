import os
import tensorflow as tf

class CnnLstmAe(tf.keras.Model):
  def __init__(self, model_file = None):
    super().__init__()
    self.model_file = model_file

  def call(self, inputs, config):
    if self.model_file != None:
      model = tf.keras.models.load_model(self.model_file)
    else:
      model = self.build_model(inputs, config)

    return model

  def build_model(self, inputs, config):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv1D(
      filters = config['conv_filters'],
      kernel_size = config['conv_kernel_size'],
      padding = 'same',
      activation = config['activation'],
      input_shape = (inputs.shape[1], 1))
    )
    model.add(tf.keras.layers.MaxPooling1D(pool_size = config['pool_size']))
    model.add(tf.keras.layers.Dropout(config['dropout']))
    model.add(tf.keras.layers.LSTM(config['lstm_nodes'], dropout = 0.2, recurrent_dropout = 0.2))
    model.add(tf.keras.layers.Dense(config['ae_code_size'], activation = config['activation']))
    model.add(tf.keras.layers.Dense(inputs.shape[1], activation = 'sigmoid'))
    optimizer = tf.keras.optimizers.Adam(learning_rate = config['learning_rate'])
    model.compile(optimizer = optimizer, loss = 'msle', metrics = ['accuracy'])
    return model

  @classmethod
  def get_weight_file(self):
    p = os.environ.get('ROOT_PATH') or ''
    return p + 'app/cnn_lstm_ae-weights.h5'
