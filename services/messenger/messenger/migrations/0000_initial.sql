CREATE TABLE msg_users (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL
)

CREATE TABLE msg_chats (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  kind TEXT NOT NULL
)

CREATE TABLE msg_groups (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  creator INTEGER NOT NULL,
  members INTEGER NOT NULL
)

CREATE TABLE msg_messages (
  id INTEGER NOT NULL PRIMARY KEY,
  chat_id INTEGER NOT NULL,
  sender_id INTEGER NOT NULL,
  text TEXT NOT NULL,
  timestamp DATETIME NOT NULL,
  is_reader BOOLEAN NOT NULL
)
