DROP TABLE IF EXISTS transaction_registry;

CREATE TABLE transaction_registry(
  id TEXT PRIMARY KEY,
  status TEXT NOT NULL
);

INSERT INTO transaction_registry(id, status) VALUES
(1, 'Success');
