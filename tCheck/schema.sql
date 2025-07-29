-- tCheck/schema.sql
DROP TABLE IF EXISTS user_completed_item;
DROP TABLE IF EXISTS user_list_assignment;
DROP TABLE IF EXISTS list_item_template;
DROP TABLE IF EXISTS list_template;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_manager BOOLEAN DEFAULT 0
);

CREATE TABLE list_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    creator_id INTEGER NOT NULL,
    is_public BOOLEAN DEFAULT 0,
    FOREIGN KEY (creator_id) REFERENCES user (id)
);

CREATE TABLE list_item_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_template_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    requires_input BOOLEAN DEFAULT 0,
    input_type TEXT,
    item_order INTEGER NOT NULL,
    FOREIGN KEY (list_template_id) REFERENCES list_template (id)
);

CREATE TABLE user_list_assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    list_template_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (list_template_id) REFERENCES list_template (id),
    UNIQUE (user_id, list_template_id)
);

CREATE TABLE user_completed_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    list_item_template_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (list_item_template_id) REFERENCES list_item_template (id),
    UNIQUE (user_id, list_item_template_id)
);