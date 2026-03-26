CREATE TABLE users (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(200),
    username VARCHAR(100) UNIQUE,
    password VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id VARCHAR(100) PRIMARY KEY,
    event_title VARCHAR(200),
    event_description VARCHAR(500),
    event_date DATE,
    event_location VARCHAR(300),
    event_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),

    CONSTRAINT fk_events_user
        FOREIGN KEY (created_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);

CREATE TABLE works (
    id VARCHAR(100) PRIMARY KEY,
    work_title VARCHAR(200),
    work_description VARCHAR(500),
    start_date DATE,
    end_date DATE,
    status VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),

    CONSTRAINT fk_works_user
        FOREIGN KEY (created_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);

CREATE TABLE gallery (
    id VARCHAR(36) PRIMARY KEY,
    photo_path TEXT,
    description TEXT,
    uploaded_at DATETIME,
    uploaded_by VARCHAR(36)
);

CREATE TABLE gov_schems (
    id VARCHAR(36) PRIMARY KEY,
    title TEXT,
    description TEXT,
    start_date date,
    end_date date,
    created_at timestamp,
    created_by varchar(200)
);
