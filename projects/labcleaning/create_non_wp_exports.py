#!/usr/bin/env python3
"""
Create export formats for non-WordPress platforms
JSON, API formats, and database-ready exports
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")

# Load data
try:
    with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'r') as f:
        services = json.load(f)
except:
    with open(DATA_DIR / "lab_cleaning_services.json", 'r') as f:
        services = json.load(f)

# 1. API-Ready JSON Format (for REST APIs)
api_format = {
    "version": "1.0",
    "generated": datetime.now().isoformat(),
    "total": len(services),
    "suppliers": []
}

for company in services:
    supplier = {
        "id": company['name'].lower().replace(' ', '-').replace(',', ''),
        "name": company['name'],
        "website": company.get('url', ''),
        "category": company.get('type', 'unknown'),
        "description": company.get('description', ''),
        "contact": {
            "emails": company.get('emails', []),
            "phones": company.get('phones', []),
            "address": company.get('address', '')
        },
        "location": {
            "city": company.get('city', ''),
            "state": company.get('state', ''),
            "zip": company.get('zip', ''),
            "country": company.get('country', 'USA')
        },
        "social": company.get('social_media', {}),
        "services": company.get('services', []),
        "metadata": {
            "founded": company.get('founded', ''),
            "employees": company.get('employees', ''),
            "revenue": company.get('revenue', ''),
            "ticker": company.get('ticker', ''),
            "parent": company.get('parent', ''),
            "certifications": company.get('certifications', [])
        },
        "last_updated": company.get('enriched_at', company.get('scraped_at', ''))
    }
    api_format["suppliers"].append(supplier)

with open(DATA_DIR / "api_suppliers.json", 'w') as f:
    json.dump(api_format, f, indent=2)

print("✅ Created: api_suppliers.json (REST API format)")

# 2. MongoDB-ready JSON
mongodb_format = []
for company in services:
    doc = {
        "_id": company['name'].lower().replace(' ', '-'),
        "name": company['name'],
        "url": company.get('url', ''),
        "type": company.get('type', ''),
        "description": company.get('description', ''),
        "contact": {
            "emails": company.get('emails', []),
            "phones": company.get('phones', []),
            "address": company.get('address', ''),
            "city": company.get('city', ''),
            "state": company.get('state', ''),
            "zip": company.get('zip', ''),
            "country": company.get('country', 'USA')
        },
        "services": company.get('services', []),
        "social_media": company.get('social_media', {}),
        "company_info": {
            "founded": company.get('founded', ''),
            "employees": company.get('employees', ''),
            "revenue": company.get('revenue', ''),
            "ticker": company.get('ticker', ''),
            "parent_company": company.get('parent', ''),
            "certifications": company.get('certifications', [])
        },
        "scraped": {
            "at": company.get('scraped_at', ''),
            "enriched_at": company.get('enriched_at', ''),
            "auto_enriched_at": company.get('auto_enriched_at', ''),
            "deep_enriched_at": company.get('deep_enriched_at', '')
        },
        "created_at": datetime.now().isoformat()
    }
    mongodb_format.append(doc)

with open(DATA_DIR / "mongodb_suppliers.json", 'w') as f:
    json.dump(mongodb_format, f, indent=2)

print("✅ Created: mongodb_suppliers.json (MongoDB import)")

# 3. Elasticsearch bulk import format
es_bulk = []
for company in services:
    doc = {
        "_index": "lab_suppliers",
        "_id": company['name'].lower().replace(' ', '-'),
        "_source": {
            "name": company['name'],
            "url": company.get('url', ''),
            "type": company.get('type', ''),
            "description": company.get('description', ''),
            "emails": company.get('emails', []),
            "phones": company.get('phones', []),
            "address": company.get('address', ''),
            "city": company.get('city', ''),
            "state": company.get('state', ''),
            "services": company.get('services', []),
            "social_media": company.get('social_media', {}),
            "founded": company.get('founded', ''),
            "employees": company.get('employees', ''),
            "revenue": company.get('revenue', ''),
            "timestamp": datetime.now().isoformat()
        }
    }
    es_bulk.append({"index": {"_index": "lab_suppliers", "_id": doc["_id"]}})
    es_bulk.append(doc["_source"])

with open(DATA_DIR / "elasticsearch_bulk.json", 'w') as f:
    for item in es_bulk:
        f.write(json.dumps(item) + '\n')

print("✅ Created: elasticsearch_bulk.json (Elasticsearch bulk import)")

# 4. GraphQL schema example
graphql_schema = """
type LabSupplier {
  id: ID!
  name: String!
  website: String!
  category: SupplierCategory!
  description: String
  contact: ContactInfo
  location: Location
  services: [String!]
  socialMedia: SocialMedia
  companyInfo: CompanyInfo
  createdAt: DateTime!
  updatedAt: DateTime!
}

type ContactInfo {
  emails: [String!]
  phones: [String!]
  address: String
}

type Location {
  city: String
  state: String
  zip: String
  country: String
  coordinates: Coordinates
}

type SocialMedia {
  linkedin: String
  twitter: String
  facebook: String
}

type CompanyInfo {
  founded: String
  employees: String
  revenue: String
  ticker: String
  parentCompany: String
  certifications: [String!]
}

type Query {
  suppliers(
    category: SupplierCategory
    state: String
    service: String
    search: String
  ): [LabSupplier!]!
  
  supplier(id: ID!): LabSupplier
  
  suppliersByState(state: String!): [LabSupplier!]!
  
  suppliersByService(service: String!): [LabSupplier!]!
}

enum SupplierCategory {
  CLEANING_SERVICE
  STERILIZATION
  CLEANING_PRODUCTS
  WASTE_MANAGEMENT
  ANALYTICAL_LAB
  TESTING_CERTIFICATION
  LAB_DECOMMISSIONING
  LAB_SERVICES
  EQUIPMENT_MANUFACTURER
  AUTOMATION
  SOFTWARE
  MARKETPLACE
}

type Mutation {
  createSupplier(input: SupplierInput!): LabSupplier!
  updateSupplier(id: ID!, input: SupplierInput!): LabSupplier!
  deleteSupplier(id: ID!): Boolean!
}
"""

with open(DATA_DIR / "graphql_schema.graphql", 'w') as f:
    f.write(graphql_schema)

print("✅ Created: graphql_schema.graphql (GraphQL schema)")

# 5. SQLite database creation script
sql_script = """
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
"""

with open(DATA_DIR / "database_schema.sql", 'w') as f:
    f.write(sql_script)

print("✅ Created: database_schema.sql (SQLite schema)")

# 6. Python import script
python_import_script = """#!/usr/bin/env python3
\"\"\"
Import lab cleaning suppliers into your application
\"\"\"

import json
import sqlite3
from pathlib import Path

# Load data
with open('lab_cleaning_services_enriched.json', 'r') as f:
    suppliers = json.load(f)

# SQLite import
def import_to_sqlite(db_path='lab_suppliers.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read schema
    with open('database_schema.sql', 'r') as f:
        schema = f.read()
    
    # Execute schema
    cursor.executescript(schema)
    
    # Import suppliers
    for supplier in suppliers:
        # Insert supplier
        cursor.execute('''
            INSERT OR REPLACE INTO suppliers 
            (name, url, type, description, address, city, state, zip, country)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            supplier.get('name'),
            supplier.get('url'),
            supplier.get('type'),
            supplier.get('description'),
            supplier.get('address'),
            supplier.get('city'),
            supplier.get('state'),
            supplier.get('zip'),
            supplier.get('country', 'USA')
        ))
        
        supplier_id = cursor.lastrowid
        
        # Insert contacts
        for email in supplier.get('emails', []):
            cursor.execute('INSERT INTO contacts (supplier_id, email) VALUES (?, ?)', (supplier_id, email))
        
        for phone in supplier.get('phones', []):
            cursor.execute('INSERT INTO contacts (supplier_id, phone) VALUES (?, ?)', (supplier_id, phone))
        
        # Insert services
        for service in supplier.get('services', []):
            cursor.execute('INSERT INTO services (supplier_id, service_name) VALUES (?, ?)', (supplier_id, service))
        
        # Insert social media
        social = supplier.get('social_media', {})
        for platform, url in social.items():
            cursor.execute('INSERT INTO social_media (supplier_id, platform, url) VALUES (?, ?, ?)', 
                       (supplier_id, platform, url))
        
        # Insert company info
        cursor.execute('''
            INSERT OR REPLACE INTO company_info 
            (supplier_id, founded, employees, revenue, ticker, parent_company)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            supplier_id,
            supplier.get('founded'),
            supplier.get('employees'),
            supplier.get('revenue'),
            supplier.get('ticker'),
            supplier.get('parent')
        ))
    
    conn.commit()
    conn.close()
    print(f'✅ Imported {len(suppliers)} suppliers to SQLite')

# MongoDB import
def import_to_mongodb(mongo_uri='mongodb://localhost:27017/'):
    from pymongo import MongoClient
    
    client = MongoClient(mongo_uri)
    db = client['lab_cleaning']
    collection = db['suppliers']
    
    with open('mongodb_suppliers.json', 'r') as f:
        suppliers = json.load(f)
    
    # Delete existing
    collection.delete_many({})
    
    # Insert new
    result = collection.insert_many(suppliers)
    
    print(f'✅ Imported {len(result.inserted_ids)} suppliers to MongoDB')

# Elasticsearch import
def import_to_elasticsearch(es_url='http://localhost:9200'):
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    
    es = Elasticsearch(es_url)
    
    with open('elasticsearch_bulk.json', 'r') as f:
        lines = f.readlines()
    
    # Bulk import
    success, failed = bulk(es, (json.loads(line) for line in lines))
    
    print(f'✅ Imported {success} suppliers to Elasticsearch')

if __name__ == '__main__':
    import_to_sqlite()
    # import_to_mongodb()
    # import_to_elasticsearch()
"""

with open(DATA_DIR / "import_script.py", 'w') as f:
    f.write(python_import_script)

print("✅ Created: import_script.py (Python import script)")

# 7. Statistics summary
stats = {
    "total_suppliers": len(services),
    "by_type": {},
    "by_state": {},
    "contact_coverage": {
        "with_email": len([s for s in services if s.get('emails')]),
        "with_phone": len([s for s in services if s.get('phones')]),
        "with_address": len([s for s in services if s.get('address')]),
        "with_social": len([s for s in services if s.get('social_media')])
    },
    "company_data": {
        "with_founded": len([s for s in services if s.get('founded')]),
        "with_employees": len([s for s in services if s.get('employees')]),
        "with_revenue": len([s for s in services if s.get('revenue')]),
        "public_companies": len([s for s in services if s.get('ticker')])
    }
}

for supplier in services:
    # Count by type
    supplier_type = supplier.get('type', 'unknown')
    stats["by_type"][supplier_type] = stats["by_type"].get(supplier_type, 0) + 1
    
    # Count by state
    state = supplier.get('state', 'unknown')
    if state and state != 'unknown':
        stats["by_state"][state] = stats["by_state"].get(state, 0) + 1

with open(DATA_DIR / "export_statistics.json", 'w') as f:
    json.dump(stats, f, indent=2)

print("✅ Created: export_statistics.json")
print(f"\n📊 Export Summary:")
print(f"  Total suppliers: {stats['total_suppliers']}")
print(f"  With email: {stats['contact_coverage']['with_email']} ({stats['contact_coverage']['with_email']/stats['total_suppliers']*100:.1f}%)")
print(f"  With phone: {stats['contact_coverage']['with_phone']} ({stats['contact_coverage']['with_phone']/stats['total_suppliers']*100:.1f}%)")
print(f"  With address: {stats['contact_coverage']['with_address']} ({stats['contact_coverage']['with_address']/stats['total_suppliers']*100:.1f}%)")
print(f"  Public companies: {stats['company_data']['public_companies']}")

print("\n✅ All non-WordPress exports complete!")
print("\nFiles created:")
print("  - api_suppliers.json (REST API format)")
print("  - mongodb_suppliers.json (MongoDB format)")
print("  - elasticsearch_bulk.json (Elasticsearch bulk)")
print("  - graphql_schema.graphql (GraphQL schema)")
print("  - database_schema.sql (SQLite schema)")
print("  - import_script.py (Python import)")
print("  - export_statistics.json (Statistics)")
