
-- Lab Suppliers Database Schema

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT,
    type TEXT,
    description TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    country TEXT DEFAULT 'USA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    email TEXT,
    phone TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    service_name TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS social_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    platform TEXT,
    url TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    founded TEXT,
    employees TEXT,
    revenue TEXT,
    ticker TEXT,
    parent_company TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_suppliers_state ON suppliers(state);
CREATE INDEX IF NOT EXISTS idx_suppliers_type ON suppliers(type);
CREATE INDEX IF NOT EXISTS idx_suppliers_city ON suppliers(city);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);
CREATE INDEX IF NOT EXISTS idx_services_name ON services(service_name);

-- Full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS suppliers_fts USING fts5(
    name, 
    description, 
    content='suppliers',
    content_rowid='id'
);

-- Triggers for full-text search sync
CREATE TRIGGER IF NOT EXISTS suppliers_fts_insert AFTER INSERT ON suppliers BEGIN
  INSERT INTO suppliers_fts(rowid, name, description)
  VALUES (new.id, new.name, new.description);
END;

CREATE TRIGGER IF NOT EXISTS suppliers_fts_delete AFTER DELETE ON suppliers BEGIN
  INSERT INTO suppliers_fts(suppliers_fts, rowid, name, description)
  VALUES ('delete', old.id, old.name, old.description);
END;

CREATE TRIGGER IF NOT EXISTS suppliers_fts_update AFTER UPDATE ON suppliers BEGIN
  INSERT INTO suppliers_fts(suppliers_fts, rowid, name, description)
  VALUES ('update', new.id, new.name, new.description);
END;
