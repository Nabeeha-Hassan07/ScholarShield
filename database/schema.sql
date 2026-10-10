-- =========================================================
-- USERS
-- =========================================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- DOCUMENTS
-- =========================================================

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    word_count INTEGER NOT NULL,
    character_count INTEGER NOT NULL,
    sentence_count INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Uploaded',

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


-- =========================================================
-- DOCUMENTS WAITING FOR ANALYSIS
-- =========================================================

CREATE TABLE IF NOT EXISTS not_analyzed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE
);


-- =========================================================
-- COMPLETED ANALYSIS SESSIONS
-- =========================================================

CREATE TABLE IF NOT EXISTS analyzed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_document_id INTEGER NOT NULL,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (original_document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE
);


-- =========================================================
-- REFERENCE DOCUMENTS FOR AN ANALYSIS
-- =========================================================

CREATE TABLE IF NOT EXISTS analysis_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    reference_document_id INTEGER NOT NULL,

    FOREIGN KEY (analysis_id)
        REFERENCES analyzed(id)
        ON DELETE CASCADE,

    FOREIGN KEY (reference_document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE,

    UNIQUE (analysis_id, reference_document_id)
);


-- =========================================================
-- NLP ANALYSIS RESULTS
-- =========================================================

CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    reference_document_id INTEGER NOT NULL,

    lexical_score REAL DEFAULT 0,
    semantic_score REAL DEFAULT 0,
    syntactic_score REAL DEFAULT 0,
    contextual_score REAL DEFAULT 0,
    meaning_score REAL DEFAULT 0,
    overall_score REAL DEFAULT 0,

    similarity_level TEXT,

    similar_passages TEXT,
    explanation TEXT,

    FOREIGN KEY (analysis_id)
        REFERENCES analyzed(id)
        ON DELETE CASCADE,

    FOREIGN KEY (reference_document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE,

    UNIQUE (analysis_id, reference_document_id)
);


-- =========================================================
-- GENERATED REPORTS
-- =========================================================

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,

    report_name TEXT NOT NULL,
    report_path TEXT NOT NULL,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (analysis_id)
        REFERENCES analyzed(id)
        ON DELETE CASCADE
);