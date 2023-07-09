CREATE TABLE IF NOT EXISTS rounds (
  id integer PRIMARY KEY,
  start_time text NOT NULL
);

CREATE TABLE IF NOT EXISTS ports (
  id integer PRIMARY KEY,
  value integer NOT NULL
);

CREATE TABLE IF NOT EXISTS rounds_ports (
  id integer PRIMARY KEY,
  round_id integer NOT NULL,
  port_id integer NOT NULL,
  timestamp text NOT NULL,
  FOREIGN KEY (round_id) REFERENCES rounds(id),
  FOREIGN KEY (port_id) REFERENCES ports(id)
);

CREATE TABLE IF NOT EXISTS packets (
  id integer PRIMARY KEY,
  timestamp text NOT NULL,
  protocols varchar(255) NOT NULL,
  qry_name varchar(255),
  resp_name varchar(255),
  port_id integer NOT NULL,
  dest_port integer NOT NULL,
  payload varchar(255),
  round_id integer NOT NULL,
  FOREIGN KEY (port_id) REFERENCES ports(id),
  FOREIGN KEY (round_id) REFERENCES rounds(id)
);

CREATE TABLE IF NOT EXISTS batches (
  id integer PRIMARY KEY,
  timestamp text NOT NULL,
  alg varchar(255)
);

CREATE TABLE IF NOT EXISTS batches_rounds (
  id integer PRIMARY KEY,
  batch_id integer NOT NULL,
  round_id integer NOT NULL,
  FOREIGN KEY (batch_id) REFERENCES batches(id),
  FOREIGN KEY (round_id) REFERENCES rounds(id)
);
