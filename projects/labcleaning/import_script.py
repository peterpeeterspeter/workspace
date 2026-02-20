#!/usr/bin/env python3
"""
Import lab cleaning suppliers into your application
"""

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
