-- =========================
-- COMPLAINS TABLE
-- =========================

CREATE TABLE IF NOT EXISTS complains (
    id VARCHAR(200),

    person_name VARCHAR(200),
    
    complain_reg_no VARCHAR(200) UNIQUE,
    
    mobile_no VARCHAR(100),
    
    address VARCHAR(200),
    
    complain_type VARCHAR(100),
    
    description TEXT,
    
    photo_path VARCHAR(300),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    status VARCHAR(100),

    INDEX idx_person_name (person_name),
    INDEX idx_mobile_no (mobile_no),
    INDEX idx_status (status)
);



-- =========================
-- EVENTS TABLE
-- =========================

CREATE TABLE IF NOT EXISTS events (
    id VARCHAR(100),

    event_title VARCHAR(200),

    event_description VARCHAR(500),

    event_date DATE,

    event_location VARCHAR(300),

    event_type VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_by VARCHAR(100),

    INDEX idx_created_by (created_by)
);



-- =========================
-- GALLERY TABLE
-- =========================

CREATE TABLE IF NOT EXISTS gallery (
    id VARCHAR(36) PRIMARY KEY,

    photo_path TEXT,

    description TEXT,

    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    uploaded_by VARCHAR(36),

    INDEX idx_uploaded_at (uploaded_at)
);



-- =========================
-- GOV_SCHEMES TABLE
-- =========================

CREATE TABLE IF NOT EXISTS gov_schemes (
    id VARCHAR(36) PRIMARY KEY,

    title TEXT,

    description TEXT,

    start_date DATE,

    end_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_by VARCHAR(200)
);



-- =========================
-- USERS TABLE
-- =========================

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(100),

    name VARCHAR(200),

    username VARCHAR(100),

    password VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_username (username)
);



-- =========================
-- WORKS TABLE
-- =========================

CREATE TABLE IF NOT EXISTS works (
    id VARCHAR(100),

    work_title VARCHAR(200),

    work_description VARCHAR(500),

    start_date DATE,

    end_date DATE,

    status VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_by VARCHAR(100),

    INDEX idx_status (status),
    INDEX idx_created_by (created_by)
);