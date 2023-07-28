import h5py
import os

class Splitter():
  def __init__(self, file):
    self.file = file
    self.chunk_size_kb = 2
    self.output_directory = '/'

  def __call__(self):
    with h5py.File(self.file, 'r') as h5_file:
      # Get the total size of the input h5 file
      total_size = os.path.getsize(self.file)

      # Calculate the number of chunks needed
      num_chunks = (total_size + self.chunk_size_kb * 1024 - 1) // (self.chunk_size_kb * 1024)

      # Create the output directory if it doesn't exist
      # os.makedirs(self.output_directory, exist_ok=True)

      # Iterate over chunks
      for chunk_idx in range(num_chunks):
        # Calculate the starting and ending byte offsets for the chunk
        start_byte = chunk_idx * self.chunk_size_kb * 1024
        end_byte = min((chunk_idx + 1) * self.chunk_size_kb * 1024, total_size)

        # Read the data for the chunk
        chunk_data = h5_file[start_byte:end_byte]

        # Create a new h5 file for the chunk
        chunk_filename = os.path.join(self.output_directory, f"{self.file}_{chunk_idx}.h5")
        with h5py.File(chunk_filename, 'w') as chunk_h5_file:
          chunk_h5_file.create_dataset("data", data=chunk_data)
