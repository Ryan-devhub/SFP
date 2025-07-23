CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

CREATE TABLE trade_posts (
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    items_offered TEXT NOT NULL,
    value REAL,
    description TEXT,
    items_wanted TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE trade_notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id INTEGER NOT NULL,
    requestor_id INTEGER NOT NULL,
    offer_message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (trade_id) REFERENCES trade_posts(trade_id),
    FOREIGN KEY (requestor_id) REFERENCES users(user_id)
);

CREATE TABLE trade_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id INTEGER NOT NULL,
    poster_id INTEGER NOT NULL,
    requestor_id INTEGER NOT NULL,
    items_offered TEXT NOT NULL,
    value REAL,
    description TEXT,
    items_wanted TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (trade_id) REFERENCES trade_posts(trade_id),
    FOREIGN KEY (poster_id) REFERENCES users(user_id),
    FOREIGN KEY (requestor_id) REFERENCES users(user_id)
);

CREATE TABLE trade_chats (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    is_accepted INTEGER NOT NULL DEFAULT 0,
    is_declined INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (trade_id) REFERENCES trade_posts(trade_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);